import T7.ProbabilityBounds
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7

theorem density_quotient_nonneg (count n power : Nat) (hn : 0 < n) :
    0 ≤ (count:Rat)/(n:Rat)^power := by
  have hp : 0 < (n:Rat)^power := Rat.pow_pos (Rat.natCast_pos.mpr hn)
  have hi := Rat.inv_pos.mpr hp
  have hnni : 0 ≤ ((n:Rat)^power)⁻¹ := by grind
  exact Rat.mul_nonneg Rat.natCast_nonneg hnni

theorem edge_density_nonneg {n : Nat} (G : SimpleHost n) (hn : 0 < n) :
    0 ≤ G.edgeDensity := density_quotient_nonneg _ _ _ hn

theorem hom_density_nonneg {n : Nat} (G : SimpleHost n) (hn : 0 < n) :
    0 ≤ G.homDensity := density_quotient_nonneg _ _ _ hn

theorem reciprocal_nat_unit (n : Nat) (hn : 0 < n) :
    0 ≤ (1/(n:Rat)) ∧ 1/(n:Rat) ≤ 1 := by
  have hnp : 0 < (n:Rat) := Rat.natCast_pos.mpr hn
  have hni : 0 < (n:Rat)⁻¹ := Rat.inv_pos.mpr hnp
  have hn0 : (n:Rat) ≠ 0 := by grind
  have hone : (1:Rat) ≤ (n:Rat) := Rat.natCast_le_natCast.mpr hn
  have hnni : 0 ≤ (n:Rat)⁻¹ := by grind
  have hm := Rat.mul_le_mul_of_nonneg_right hone hnni
  have hc := Rat.mul_inv_cancel (n:Rat) hn0
  grind

/-- Strongest host theorem in this project. Jensen and Bernoulli are proved internally.
The rational outcome distribution and its two sampling estimates remain explicit inputs. -/
theorem finite_host_conditional {n : Nat} (hn : 0 < n)
    (outcomes : List (SimpleHost n)) (weight : SimpleHost n → Rat)
    (mu kernelDensity delta : Rat)
    (hw : ∀ G ∈ outcomes, 0 ≤ weight G)
    (hnorm : (outcomes.map weight).sum = 1)
    (hmu : 0 ≤ mu)
    (hdelta : delta = mu^30-kernelDensity)
    (hdeltaPos : 0 < delta)
    (hsize : (136+30*mu^30)/delta < (n:Rat))
    (hcollision : expectation outcomes weight SimpleHost.homDensity ≤ kernelDensity+136*(1/(n:Rat)))
    (hmean : expectation outcomes weight SimpleHost.edgeDensity = (1-1/(n:Rat))*mu) :
    ∃ G ∈ outcomes, G.homDensity < G.edgeDensity^30 ∧ 0 < G.edgeDensity := by
  have hunit := reciprocal_nat_unit n hn
  have hb := host_bernoulli mu (1/(n:Rat)) hmu hunit.1 hunit.2
  have hj := finite_jensen_30 outcomes weight SimpleHost.edgeDensity hw
    (fun G _ => edge_density_nonneg G hn) hnorm
  have hs := sufficient_host_size mu delta (n:Rat) hdeltaPos (Rat.natCast_pos.mpr hn) hsize
  obtain ⟨G,hG,hdef⟩ := finite_host_from_sampling_bounds outcomes weight mu kernelDensity delta
    (1/(n:Rat)) hw hdelta hs hcollision hmean hb hj
  refine ⟨G,hG,hdef,?_⟩
  have he := edge_density_nonneg G hn
  have ht := hom_density_nonneg G hn
  by_cases hp : 0 < G.edgeDensity
  · exact hp
  · have hz : G.edgeDensity = 0 := by grind
    rw [hz] at hdef
    grind

end T7
