import T7.FiniteHost
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7

theorem rational_bernoulli (u : Rat) (hu0 : 0 ≤ u) (hu1 : u ≤ 1) (n : Nat) :
    1-(n:Rat)*u ≤ (1-u)^n := by
  induction n with
  | zero => simp; decide +kernel
  | succ n ih =>
    have hnon : 0 ≤ 1-u := by grind
    have hstep := Rat.mul_le_mul_of_nonneg_right ih hnon
    have hnn : 0 ≤ (n:Rat) := Rat.natCast_nonneg
    have hs := Rat.mul_nonneg hnn (Rat.mul_nonneg hu0 hu0)
    rw [Rat.pow_succ]
    grind

theorem host_bernoulli (mu u : Rat) (hmu : 0 ≤ mu) (hu0 : 0 ≤ u) (hu1 : u ≤ 1) :
    (1-30*u)*mu^30 ≤ ((1-u)*mu)^30 := by
  have hb := rational_bernoulli u hu0 hu1 30
  have hp := Rat.mul_le_mul_of_nonneg_right hb (Rat.pow_nonneg (n := 30) hmu)
  grind

theorem sum_rat_nonneg (l : List α) (f : α → Rat)
    (h : ∀ x ∈ l, 0 ≤ f x) : 0 ≤ (l.map f).sum := by
  induction l with
  | nil => simp
  | cons x xs ih =>
    have h0 := h x (by simp)
    have h1 := ih (fun y hy => h y (by simp [hy]))
    simp only [List.map_cons, List.sum_cons]
    grind

def tangentRemainder (x y : Rat) : Rat :=
  ((List.range 29).map fun k => ((k+1:Nat):Rat)*x^(28-k)*y^k).sum

theorem tangent_remainder_nonneg (x y : Rat) (hx : 0 ≤ x) (hy : 0 ≤ y) :
    0 ≤ tangentRemainder x y := by
  apply sum_rat_nonneg
  intro k _
  exact Rat.mul_nonneg (Rat.mul_nonneg Rat.natCast_nonneg (Rat.pow_nonneg hx)) (Rat.pow_nonneg hy)

theorem tangent_identity (x y : Rat) :
    x^30-y^30-30*y^29*(x-y) = (x-y)^2*tangentRemainder x y := by
  simp [tangentRemainder, List.range_succ]
  grind

theorem tangent_inequality (x y : Rat) (hx : 0 ≤ x) (hy : 0 ≤ y) :
    y^30+30*y^29*(x-y) ≤ x^30 := by
  have hs : 0 ≤ (x-y)^2 := by
    by_cases h : 0 ≤ x-y
    · exact Rat.pow_nonneg h
    · have h' : 0 ≤ y-x := by grind
      have hp := Rat.mul_nonneg h' h'
      grind
  have hr := Rat.mul_nonneg hs (tangent_remainder_nonneg x y hx hy)
  rw [← tangent_identity] at hr
  grind

theorem expectation_affine (l : List α) (w f : α → Rat) (a b : Rat) :
    expectation l w (fun x => a+b*f x) = a*(l.map w).sum+b*expectation l w f := by
  induction l with
  | nil => simp [expectation]; decide +kernel
  | cons x xs ih =>
    simp only [expectation, List.map_cons, List.sum_cons] at ih ⊢
    grind

/-- Finite rational Jensen at the exact exponent required by the packet. -/
theorem finite_jensen_30 (l : List α) (w f : α → Rat)
    (hw : ∀ x ∈ l, 0 ≤ w x) (hf : ∀ x ∈ l, 0 ≤ f x)
    (hnorm : (l.map w).sum = 1) :
    (expectation l w f)^30 ≤ expectation l w (fun x => (f x)^30) := by
  let m := expectation l w f
  have hm : 0 ≤ m := sum_rat_nonneg l (fun x => w x*f x)
    (fun x hx => Rat.mul_nonneg (hw x hx) (hf x hx))
  have hle : ∀ x ∈ l, w x*(m^30+30*m^29*(f x-m)) ≤ w x*(f x)^30 := by
    intro x hx
    exact Rat.mul_le_mul_of_nonneg_left (tangent_inequality (f x) m (hf x hx) hm) (hw x hx)
  have hs := sum_rat_le l _ _ hle
  have he : expectation l w (fun x => m^30+30*m^29*(f x-m)) = m^30 := by
    have hfun : (fun x => m^30+30*m^29*(f x-m)) =
        (fun x => (m^30-30*m^30)+(30*m^29)*f x) := by funext x; grind
    rw [hfun, expectation_affine, hnorm]
    change _ + _ * m = m^30
    grind
  change expectation l w _ ≤ expectation l w _ at hs
  rw [he] at hs
  exact hs

end T7
