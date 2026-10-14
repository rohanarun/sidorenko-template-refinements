import T7Gap.FiniteProbability
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

/-- Finite signed base kernels. These hypotheses express positivity and mean one, not a deficit. -/
structure SignedBase (X Y : Type) where
  left : FiniteLaw X
  right : FiniteLaw Y
  value : Bool → X → Y → Rat
  nonnegative : ∀ sign x y, 0 ≤ value sign x y
  mean_one : ∀ sign, left.mean (fun x => right.mean (value sign x)) = 1

theorem independent_bipartite_product (left : FiniteLaw X) (right : FiniteLaw Y)
    (n : Nat) (f : Fin n → X → Y → Rat) :
    (independentLaw left n).mean (fun x => (independentLaw right n).mean
      (fun y => coordinateProduct (fun i => f i (x i) (y i)))) =
    coordinateProduct (fun i => left.mean (fun x => right.mean (f i x))) := by
  have he : (fun x : Fin n → X => (independentLaw right n).mean
      (fun y => coordinateProduct (fun i => f i (x i) (y i)))) =
      (fun x => coordinateProduct (fun i => right.mean (f i (x i)))) := by
    funext x
    exact independent_product right n (fun i y => f i (x i) y)
  rw [he]
  exact independent_product left n (fun i x => right.mean (f i x))

/-- The actual activation construction for one incident type pair, with thirty independent coordinates. -/
def activationKernel (base : SignedBase X Y) (c : Corner)
    (x : Fin 30 → X) (y : Fin 30 → Y) : Rat :=
  (activationLaw c).mean (fun o => coordinateProduct (fun i =>
    if activationSupport c o.1 i then base.value (o.2 i) (x i) (y i) else 1))

theorem activationKernel_nonnegative (base : SignedBase X Y) (c : Corner)
    (x : Fin 30 → X) (y : Fin 30 → Y) : 0 ≤ activationKernel base c x y := by
  apply FiniteLaw.mean_nonneg
  intro o _
  apply coordinateProduct_nonneg
  intro i
  split
  · exact base.nonnegative _ _ _
  · decide +kernel

theorem activationKernel_mean_one (base : SignedBase X Y) (c : Corner) :
    (independentLaw base.left 30).mean (fun x =>
      (independentLaw base.right 30).mean (activationKernel base c x)) = 1 := by
  unfold activationKernel
  have he : (fun x : Fin 30 → X => (independentLaw base.right 30).mean (fun y =>
      (activationLaw c).mean (fun o => coordinateProduct (fun i =>
        if activationSupport c o.1 i then base.value (o.2 i) (x i) (y i) else 1)))) =
      (fun x => (activationLaw c).mean (fun o => (independentLaw base.right 30).mean (fun y =>
        coordinateProduct (fun i => if activationSupport c o.1 i then base.value (o.2 i) (x i) (y i) else 1)))) := by
    funext x
    exact FiniteLaw.mean_comm _ _ _
  rw [he,FiniteLaw.mean_comm]
  have hi : (fun o : ActivationOutcome => (independentLaw base.left 30).mean (fun x =>
      (independentLaw base.right 30).mean (fun y => coordinateProduct (fun i =>
        if activationSupport c o.1 i then base.value (o.2 i) (x i) (y i) else 1)))) =
      (fun _ => (1:Rat)) := by
    funext o
    rw [independent_bipartite_product base.left base.right 30
      (fun i x y => if activationSupport c o.1 i then base.value (o.2 i) x y else 1)]
    have hf : (fun i : Fin 30 => base.left.mean (fun x => base.right.mean (fun y =>
        if activationSupport c o.1 i then base.value (o.2 i) x y else 1))) = (fun _ => (1:Rat)) := by
      funext i
      by_cases h : activationSupport c o.1 i = true
      · simp only [h,ite_true]; exact base.mean_one _
      · simp [h,FiniteLaw.mean_const]
    rw [hf,coordinateProduct_one]
  rw [hi,FiniteLaw.mean_const]

/-- A genuine finite kernel with its space and entries, not a freely supplied density scalar. -/
structure RationalBipartiteKernel (X Y : Type) where
  left : FiniteLaw X
  right : FiniteLaw Y
  value : X → Y → Rat
  nonnegative : ∀ x y, 0 ≤ value x y

def RationalBipartiteKernel.mean (W : RationalBipartiteKernel X Y) : Rat :=
  W.left.mean (fun x => W.right.mean (W.value x))

def RationalBipartiteKernel.density (W : RationalBipartiteKernel X Y) : Rat :=
  (independentLaw W.left 7).mean (fun x => (independentLaw W.right 10).mean
    (fun y => coordinateProduct (fun c : Corner => W.value (x (corner c).1) (y (corner c).2))))

def incidentActivationKernel (base : SignedBase X Y) (c : Corner) :
    RationalBipartiteKernel (Fin 30 → X) (Fin 30 → Y) where
  left := independentLaw base.left 30
  right := independentLaw base.right 30
  value := activationKernel base c
  nonnegative := activationKernel_nonnegative base c

theorem incidentActivationKernel_mean (base : SignedBase X Y) (c : Corner) :
    (incidentActivationKernel base c).mean = 1 := activationKernel_mean_one base c

/-- A legitimate instance shows the base-kernel hypotheses are consistent. It makes no deficit claim. -/
def unitLaw : FiniteLaw Unit where
  outcomes := [()]
  weight := fun _ => 1
  nonnegative := by intro _ _; decide +kernel
  normalized := by decide +kernel

def unitSignedBase : SignedBase Unit Unit where
  left := unitLaw
  right := unitLaw
  value := fun _ _ _ => 1
  nonnegative := by intro _ _ _; decide +kernel
  mean_one := by intro _; rw [FiniteLaw.mean_const,FiniteLaw.mean_const]

theorem kernel_construction_has_instance (c : Corner) :
    (incidentActivationKernel unitSignedBase c).mean = 1 := incidentActivationKernel_mean _ c

end T7Gap
