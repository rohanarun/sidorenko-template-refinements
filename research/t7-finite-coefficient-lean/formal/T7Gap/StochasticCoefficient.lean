import T7Gap.Marginal
import T7.MomentBridge
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

/-- Full source sum with actual probability expectations at every corner. -/
def stochasticCoefficient (target : Corner → Corner) : Rat :=
  (allLabelings.map fun a => ((List.finRange 30).map fun c =>
    activationMoment (target c) (a (leftEdge c)) (a (rightEdge c))).prod).sum

theorem stochastic_identity_eq_fullCoefficient : stochasticCoefficient id = fullCoefficient := by
  unfold stochasticCoefficient
  simp only [activation_moment_eq_formula,id_eq]
  exact full_coefficient_is_sum_of_products.symm

theorem stochastic_reversal_eq_fullCoefficient :
    stochasticCoefficient reverseCorner = reverseFullCoefficient := by
  unfold stochasticCoefficient
  simp only [activation_moment_eq_formula]
  exact reverse_coefficient_is_sum_of_products.symm

theorem stochastic_identity_coefficient : stochasticCoefficient id = -(1/4^30:Rat) := by
  rw [stochastic_identity_eq_fullCoefficient,full_coefficient_exact]

theorem stochastic_reversal_coefficient : stochasticCoefficient reverseCorner = -(1/4^30:Rat) := by
  rw [stochastic_reversal_eq_fullCoefficient,reverse_full_coefficient_exact]

theorem stochastic_signed_orbit :
    stochasticCoefficient id+stochasticCoefficient reverseCorner = -(1/2^59:Rat) := by
  rw [stochastic_identity_eq_fullCoefficient,stochastic_reversal_eq_fullCoefficient,signed_orbit_coefficient]

/-- The activation-law assumptions have actual values at every one of the thirty corners. -/
theorem activation_law_exists (c : Corner) : ∃ law : FiniteLaw ActivationOutcome,
    law.outcomes = activationOutcomes ∧ law.weight = activationWeight c ∧
    ∀ a b : Mask, law.mean (fun o => phi c a o*phi c b o) = moment c a b := by
  exact ⟨activationLaw c,rfl,rfl,activation_moment_eq_formula c⟩

end T7Gap
