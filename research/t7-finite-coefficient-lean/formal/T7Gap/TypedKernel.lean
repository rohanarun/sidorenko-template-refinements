import T7Gap.Priors
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

def cornerIndex (p : Point) (j : Face) : Corner :=
  ((List.finRange 30).find? fun c => corner c == (p,j)).getD 0

theorem cornerIndex_valid : ∀ p j, incident p j = true → corner (cornerIndex p j) = (p,j) := by decide +kernel

def pairKernel (base : SignedBase X Y) (p : Point) (j : Face)
    (x : Fin 30 → X) (y : Fin 30 → Y) : Rat :=
  if incident p j then activationKernel base (cornerIndex p j) x y else 1

def thinnedPairKernel (base : SignedBase X Y) (p : Point) (j : Face)
    (x : Fin 30 → X) (y : Fin 30 → Y) : Rat :=
  thinning p j*pairKernel base p j x y+(1-thinning p j)

theorem pairKernel_nonnegative (base : SignedBase X Y) (p : Point) (j : Face)
    (x : Fin 30 → X) (y : Fin 30 → Y) : 0 ≤ pairKernel base p j x y := by
  unfold pairKernel
  split
  · exact activationKernel_nonnegative _ _ _ _
  · decide +kernel

theorem pairKernel_mean (base : SignedBase X Y) (p : Point) (j : Face) :
    (independentLaw base.left 30).mean (fun x => (independentLaw base.right 30).mean (pairKernel base p j x)) = 1 := by
  change (independentLaw base.left 30).mean (fun x => (independentLaw base.right 30).mean (fun y => pairKernel base p j x y)) = 1
  unfold pairKernel
  by_cases h : incident p j = true
  · simp only [h,ite_true]
    exact activationKernel_mean_one base (cornerIndex p j)
  · simp [h,FiniteLaw.mean_const]

theorem thinnedPairKernel_nonnegative (base : SignedBase X Y) (p : Point) (j : Face)
    (x : Fin 30 → X) (y : Fin 30 → Y) : 0 ≤ thinnedPairKernel base p j x y := by
  have h := thinning_bounds p j
  have h0 : 0 ≤ thinning p j := by grind only
  have hprod := Rat.mul_nonneg h0 (pairKernel_nonnegative base p j x y)
  unfold thinnedPairKernel
  grind only

theorem thinnedPairKernel_mean (base : SignedBase X Y) (p : Point) (j : Face) :
    (independentLaw base.left 30).mean (fun x => (independentLaw base.right 30).mean (thinnedPairKernel base p j x)) = 1 := by
  unfold thinnedPairKernel
  simp only [FiniteLaw.mean_add,FiniteLaw.mean_mul,FiniteLaw.mean_const]
  rw [pairKernel_mean]
  grind only

/-- Source types, thirty independent coordinates, exact beta priors and thinning, all as finite data. -/
def constructedKernel (base : SignedBase X Y) :
    RationalBipartiteKernel (Point × (Fin 30 → X)) (Face × (Fin 30 → Y)) where
  left := productLaw pointPrior (independentLaw base.left 30)
  right := productLaw facePrior (independentLaw base.right 30)
  value := fun x y => thinnedPairKernel base x.1 y.1 x.2 y.2
  nonnegative := fun x y => thinnedPairKernel_nonnegative base x.1 y.1 x.2 y.2

theorem constructedKernel_mean_one (base : SignedBase X Y) : (constructedKernel base).mean = 1 := by
  change (productLaw pointPrior (independentLaw base.left 30)).mean
    (fun x => (productLaw facePrior (independentLaw base.right 30)).mean
      (fun y => thinnedPairKernel base x.1 y.1 x.2 y.2)) = 1
  simp only [productLaw_mean]
  have hp (p : Point) : (independentLaw base.left 30).mean (fun x => facePrior.mean
      (fun j => (independentLaw base.right 30).mean (thinnedPairKernel base p j x))) = 1 := by
    rw [FiniteLaw.mean_comm]
    simp only [thinnedPairKernel_mean,FiniteLaw.mean_const]
  simp only [hp,FiniteLaw.mean_const]

theorem constructed_symmetric_mean_one (base : SignedBase X Y) :
    (symmetricProductKernel (constructedKernel base)).mean = 1 := by
  rw [symmetricProduct_mean,constructedKernel_mean_one]
  decide +kernel

/-- Nonconstant signed kernels provide a second concrete, legitimate instance of construction inputs. -/
def booleanLaw : FiniteLaw Bool where
  outcomes := [false,true]
  weight := fun _ => 1/2
  nonnegative := by intro _ _; decide +kernel
  normalized := by decide +kernel

def booleanSignedBase : SignedBase Bool Bool where
  left := booleanLaw
  right := booleanLaw
  value := fun sign x y => if xor x y == sign then 2 else 0
  nonnegative := by decide +kernel
  mean_one := by decide +kernel

theorem boolean_constructed_mean : (constructedKernel booleanSignedBase).mean = 1 :=
  constructedKernel_mean_one _

theorem boolean_sign_values :
    booleanSignedBase.value false false false = 2 ∧
    booleanSignedBase.value false false true = 0 ∧
    booleanSignedBase.value true false false = 0 ∧
    booleanSignedBase.value true false true = 2 := by decide +kernel

end T7Gap
