import T7.Orbit
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7

/-- Small arithmetic used by the packet. This does not establish the analytic rank-layer law. -/
theorem packet_constants :
    (7^7 * 10^10 : Nat) < 2^54 ∧
    (2^30-1)^15 < (2^450 : Nat) ∧
    (37*136+34 : Nat) = 5066 ∧
    (30*446-5066 : Nat) = 8314 ∧
    (4104*10*(3+1)^2 : Nat) = 656640 ∧
    (12*656640^2+2*656640 : Nat) = 5174114388480 ∧
    (656640+20*5174114388480 : Nat) = 103482288426240 ∧
    (103482288426242 : Nat) % 2 = 0 := by decide +kernel

/-- The lower-score remainder bound is an explicit premise here. -/
theorem normalized_orbit_dominance (remainder : Rat)
    (h : remainder < 1 / 2^60) :
    fullCoefficient + reverseFullCoefficient + remainder < -(1 / 2^60 : Rat) := by
  rw [signed_orbit_coefficient]
  have hc : (1 / 2^59 : Rat) = 2 * (1 / 2^60 : Rat) := by decide +kernel
  rw [hc]
  grind

theorem interval_product_upper (a b B : Rat)
    (hB : 0 ≤ B) (ha0 : -B ≤ a) (ha1 : a ≤ B)
    (hb0 : -B ≤ b) (hb1 : b ≤ B) : a*b ≤ B*B := by
  by_cases hb : 0 ≤ b
  · have h1 := Rat.mul_le_mul_of_nonneg_right ha1 hb
    have h2 := Rat.mul_le_mul_of_nonneg_left hb1 hB
    grind
  · have hn : 0 ≤ -b := by grind
    have h1 := Rat.mul_le_mul_of_nonneg_right ha0 hn
    have h2 := Rat.mul_le_mul_of_nonneg_left (Rat.neg_le_neg hb0) hB
    grind

theorem unit_power (x : Rat) (hx0 : 0 ≤ x) (hx1 : x ≤ 1) (n : Nat) :
    0 ≤ x^n ∧ x^n ≤ 1 := by
  induction n with
  | zero => simp; decide
  | succ n ih =>
    rw [Rat.pow_succ]
    have h1 := Rat.mul_nonneg ih.1 hx0
    have h2 := Rat.mul_le_mul_of_nonneg_right ih.2 hx0
    grind

/-- Algebraic dilution step, with coefficient and smallness assumptions stated as parameters. -/
theorem dilution_deficit (t0 t1 B eta eps : Rat)
    (hB : 0 ≤ B) (heps0 : 0 < eps) (heps1 : eps ≤ 1)
    (ht0 : t0 ≤ -eta) (ht0lo : -B ≤ t0) (ht0hi : t0 ≤ B)
    (ht1lo : -B ≤ t1) (ht1hi : t1 ≤ B)
    (hsmall : eps^3*B*(1+B) < eta/4) :
    (1+eps^7*t0)*(1+eps^10*t1) < 1-3*eta*eps^7/4 := by
  have hep : 0 ≤ eps := by grind
  have h3 := Rat.pow_nonneg (n := 3) hep
  have h7 := Rat.pow_pos (n := 7) heps0
  have h10 := Rat.pow_nonneg (n := 10) hep
  have hpow := (unit_power eps hep heps1 7).2
  have h10le : eps^10 ≤ eps^3 := by
    have hh := Rat.mul_le_mul_of_nonneg_left hpow h3
    grind
  have hprod := interval_product_upper t0 t1 B hB ht0lo ht0hi ht1lo ht1hi
  have hB2 := Rat.mul_nonneg hB hB
  have ht1 := Rat.mul_le_mul_of_nonneg_left ht1hi h3
  have htprod := Rat.mul_le_mul_of_nonneg_left hprod h10
  have hlast := Rat.mul_le_mul_of_nonneg_right h10le hB2
  have hcoef : t0+eps^3*t1+eps^10*t0*t1 < -3*eta/4 := by grind
  have hfinal := Rat.mul_lt_mul_of_pos_left hcoef h7
  grind

/-- Sufficient numerical error condition; deriving it from RL is not assumed implicitly. -/
theorem product_error_budget (limit actual eta eps error : Rat)
    (hl : limit ≤ 1-eta*eps^7/2)
    (ha : actual ≤ limit + error)
    (he : error < eta*eps^7/4) :
    actual < 1-eta*eps^7/4 := by grind

/-- Scaling a rational density deficit. Kernel construction and factorization remain separate obligations. -/
theorem scale_deficit (density L : Rat) (hL : 0 < L) (hd : density < 1) :
    density / L^30 < (1/L)^30 := by
  have hp := Rat.pow_pos (n := 30) hL
  apply (Rat.div_lt_iff hp).mpr
  have hn : L ≠ 0 := by grind
  have hi := Rat.mul_inv_cancel L hn
  have he : (1/L)^30 * L^30 = 1 := by grind
  rw [he]
  exact hd

end T7
