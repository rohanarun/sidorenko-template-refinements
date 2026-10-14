import T7Gap.GeneralCoefficient
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

theorem coordinateProduct_const (r : Rat) (n : Nat) : coordinateProduct (fun _ : Fin n => r) = r^n := by
  induction n with
  | zero => simp [coordinateProduct]
  | succ n ih => simp only [coordinateProduct,ih,Rat.pow_succ]; grind only

def scaleKernel (W : RationalBipartiteKernel X Y) (r : Rat) (hr : 0 ≤ r) : RationalBipartiteKernel X Y where
  left := W.left
  right := W.right
  value := fun x y => r*W.value x y
  nonnegative := fun x y => Rat.mul_nonneg hr (W.nonnegative x y)

theorem scaleKernel_mean (W : RationalBipartiteKernel X Y) (r : Rat) (hr : 0 ≤ r) :
    (scaleKernel W r hr).mean = r*W.mean := by
  unfold RationalBipartiteKernel.mean scaleKernel
  simp only [FiniteLaw.mean_mul]

theorem scaleKernel_density (W : RationalBipartiteKernel X Y) (r : Rat) (hr : 0 ≤ r) :
    (scaleKernel W r hr).density = r^30*W.density := by
  unfold RationalBipartiteKernel.density scaleKernel
  simp only [coordinateProduct_mul,coordinateProduct_const,FiniteLaw.mean_mul]

theorem rat_member_le_sum (xs : List Rat) (hn : ∀ x ∈ xs, 0 ≤ x) (x : Rat) (hx : x ∈ xs) : x ≤ xs.sum := by
  induction xs with
  | nil => simp at hx
  | cons y ys ih =>
    have hy := hn y (by simp)
    have ht : ∀ z ∈ ys, 0 ≤ z := fun z hz => hn z (by simp [hz])
    have hsum : 0 ≤ ys.sum := by simpa using sum_rat_nonneg ys id ht
    rcases List.mem_cons.mp hx with he | he
    · subst x
      simp only [List.sum_cons]
      grind only
    · have hb := ih ht he
      simp only [List.sum_cons]
      grind only

def kernelValues (W : RationalBipartiteKernel X Y) : List Rat :=
  W.left.outcomes.flatMap fun x => W.right.outcomes.map (W.value x)
def kernelBound (W : RationalBipartiteKernel X Y) : Rat := 1+(kernelValues W).sum

theorem kernelValues_nonnegative (W : RationalBipartiteKernel X Y) : ∀ r ∈ kernelValues W, 0 ≤ r := by
  intro r hr
  obtain ⟨x,hx,hr⟩ := List.mem_flatMap.mp hr
  obtain ⟨y,hy,rfl⟩ := List.mem_map.mp hr
  exact W.nonnegative x y

theorem kernelBound_positive (W : RationalBipartiteKernel X Y) : 0 < kernelBound W := by
  have h : 0 ≤ (kernelValues W).sum := by simpa using sum_rat_nonneg (kernelValues W) id (kernelValues_nonnegative W)
  unfold kernelBound
  grind only

theorem kernelBound_covers (W : RationalBipartiteKernel X Y) (x : X) (y : Y)
    (hx : x ∈ W.left.outcomes) (hy : y ∈ W.right.outcomes) : W.value x y ≤ kernelBound W := by
  have hm : W.value x y ∈ kernelValues W := List.mem_flatMap.mpr ⟨x,hx,List.mem_map.mpr ⟨y,hy,rfl⟩⟩
  have h := rat_member_le_sum _ (kernelValues_nonnegative W) _ hm
  unfold kernelBound
  grind only

def boundedKernel (W : RationalBipartiteKernel X Y) : RationalBipartiteKernel X Y :=
  scaleKernel W (kernelBound W)⁻¹ (by have h := Rat.inv_pos.mpr (kernelBound_positive W); grind only)

theorem boundedKernel_unit_interval (W : RationalBipartiteKernel X Y) (x : X) (y : Y)
    (hx : x ∈ W.left.outcomes) (hy : y ∈ W.right.outcomes) :
    0 ≤ (boundedKernel W).value x y ∧ (boundedKernel W).value x y ≤ 1 := by
  refine ⟨(boundedKernel W).nonnegative x y,?_⟩
  have hp := kernelBound_positive W
  have hi : 0 ≤ (kernelBound W)⁻¹ := by have h := Rat.inv_pos.mpr hp; grind only
  have hz : kernelBound W ≠ 0 := by grind only
  have hc := Rat.mul_inv_cancel (kernelBound W) hz
  have h := Rat.mul_le_mul_of_nonneg_right (kernelBound_covers W x y hx hy) hi
  change (kernelBound W)⁻¹*W.value x y ≤ 1
  grind only

theorem boundedKernel_mean (W : RationalBipartiteKernel X Y) :
    (boundedKernel W).mean = (kernelBound W)⁻¹*W.mean := scaleKernel_mean _ _ _

theorem boundedKernel_density (W : RationalBipartiteKernel X Y) :
    (boundedKernel W).density = ((kernelBound W)⁻¹)^30*W.density := scaleKernel_density _ _ _

theorem boundedKernel_symmetric (W : RationalBipartiteKernel X X) (h : ∀ x y, W.value x y = W.value y x) :
    ∀ x y, (boundedKernel W).value x y = (boundedKernel W).value y x := by
  intro x y
  change (kernelBound W)⁻¹*W.value x y = (kernelBound W)⁻¹*W.value y x
  rw [h]

/-- Actual bounded rational symmetric kernel; no deficit is asserted. -/
def boundedConstructedKernel (base : SignedBase X Y) := boundedKernel (symmetricProductKernel (constructedKernel base))

theorem boundedConstructed_mean_positive (base : SignedBase X Y) :
    0 < (boundedConstructedKernel base).mean := by
  unfold boundedConstructedKernel
  rw [boundedKernel_mean,constructed_symmetric_mean_one,Rat.mul_one]
  exact Rat.inv_pos.mpr (kernelBound_positive _)

end T7Gap
