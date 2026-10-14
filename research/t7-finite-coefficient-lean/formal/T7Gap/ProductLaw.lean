import T7Gap.ActivationKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

def pairOutcomes (left : FiniteLaw X) (right : FiniteLaw Y) : List (X × Y) :=
  left.outcomes.flatMap fun x => right.outcomes.map fun y => (x,y)
def pairWeight (left : FiniteLaw X) (right : FiniteLaw Y) (p : X × Y) : Rat :=
  left.weight p.1*right.weight p.2

theorem pair_sum (left : FiniteLaw X) (right : FiniteLaw Y) (f : X × Y → Rat) :
    ((pairOutcomes left right).map fun p => pairWeight left right p*f p).sum =
    left.mean (fun x => right.mean (fun y => f (x,y))) := by
  unfold pairOutcomes FiniteLaw.mean
  simp only [List.map_flatMap,List.map_map,Function.comp_def,rat_sum_flatMap]
  congr 1
  apply List.map_congr_left
  intro x _
  rw [← rat_sum_mul]
  congr 1
  apply List.map_congr_left
  intro y _
  unfold pairWeight
  grind only

def productLaw (left : FiniteLaw X) (right : FiniteLaw Y) : FiniteLaw (X × Y) where
  outcomes := pairOutcomes left right
  weight := pairWeight left right
  nonnegative := by
    intro p hp
    obtain ⟨x,hx,hp⟩ := List.mem_flatMap.mp hp
    obtain ⟨y,hy,rfl⟩ := List.mem_map.mp hp
    exact Rat.mul_nonneg (left.nonnegative x hx) (right.nonnegative y hy)
  normalized := by
    have h := pair_sum left right (fun _ => 1)
    simp only [Rat.mul_one,FiniteLaw.mean_const] at h
    exact h

theorem productLaw_mean (left : FiniteLaw X) (right : FiniteLaw Y) (f : X × Y → Rat) :
    (productLaw left right).mean f = left.mean (fun x => right.mean (fun y => f (x,y))) := pair_sum _ _ _

/-- Actual symmetric product kernel from source section 8. -/
def symmetricProductValue (W : RationalBipartiteKernel X Y) (p q : X × Y) : Rat :=
  W.value p.1 q.2*W.value q.1 p.2

theorem symmetricProduct_symmetric (W : RationalBipartiteKernel X Y) (p q : X × Y) :
    symmetricProductValue W p q = symmetricProductValue W q p := by
  unfold symmetricProductValue
  grind only

theorem symmetricProduct_nonnegative (W : RationalBipartiteKernel X Y) (p q : X × Y) :
    0 ≤ symmetricProductValue W p q := Rat.mul_nonneg (W.nonnegative _ _) (W.nonnegative _ _)

def symmetricProductKernel (W : RationalBipartiteKernel X Y) : RationalBipartiteKernel (X × Y) (X × Y) where
  left := productLaw W.left W.right
  right := productLaw W.left W.right
  value := symmetricProductValue W
  nonnegative := symmetricProduct_nonnegative W

/-- Mean is computed from actual kernel entries and product-space weights. -/
theorem symmetricProduct_mean (W : RationalBipartiteKernel X Y) :
    (symmetricProductKernel W).mean = W.mean*W.mean := by
  change (productLaw W.left W.right).mean (fun p =>
    (productLaw W.left W.right).mean (fun q => W.value p.1 q.2*W.value q.1 p.2)) = W.mean*W.mean
  simp only [productLaw_mean]
  have hin (x : X) (y : Y) :
      W.left.mean (fun x' => W.right.mean (fun y' => W.value x y'*W.value x' y)) =
      W.left.mean (fun x' => W.value x' y)*W.right.mean (fun y' => W.value x y') := by
    have hfun : (fun x' => W.right.mean (fun y' => W.value x y'*W.value x' y)) =
        (fun x' => W.value x' y*W.right.mean (fun y' => W.value x y')) := by
      funext x'
      have hc : (fun y' => W.value x y'*W.value x' y) = (fun y' => W.value x' y*W.value x y') := by funext y'; grind only
      rw [hc,FiniteLaw.mean_mul]
    rw [hfun]
    have hc : (fun x' => W.value x' y*W.right.mean (fun y' => W.value x y')) =
        (fun x' => W.right.mean (fun y' => W.value x y')*W.value x' y) := by funext x'; grind only
    rw [hc,FiniteLaw.mean_mul]
    grind only
  simp only [hin]
  have hin2 (x : X) : W.right.mean (fun y => W.left.mean (fun x' => W.value x' y)*W.right.mean (fun y' => W.value x y')) =
      W.right.mean (fun y' => W.value x y')*W.mean := by
    have hc : (fun y => W.left.mean (fun x' => W.value x' y)*W.right.mean (fun y' => W.value x y')) =
        (fun y => W.right.mean (fun y' => W.value x y')*W.left.mean (fun x' => W.value x' y)) := by funext y; grind only
    rw [hc,FiniteLaw.mean_mul,FiniteLaw.mean_comm]
    rfl
  simp only [hin2]
  have hc : (fun x => W.right.mean (fun y' => W.value x y')*W.mean) =
      (fun x => W.mean*W.right.mean (fun y' => W.value x y')) := by funext x; grind only
  rw [hc,FiniteLaw.mean_mul]
  rfl

end T7Gap
