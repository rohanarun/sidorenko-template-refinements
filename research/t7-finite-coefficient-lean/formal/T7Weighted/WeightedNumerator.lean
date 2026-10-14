import T7Weighted.CoefficientBounds
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Weighted
open T7 T7Gap

abbrev TypeMap := (Point → Point) × (Face → Face)
noncomputable instance : DecidableEq TypeMap := Classical.typeDecidableEq _
def identityMap : TypeMap := (id,id)
def reversalMap : TypeMap := (reversePoint,reverseFace)
def allTypeMaps : List TypeMap := (functions (List.finRange 7) 7).flatMap fun a =>
  (functions (List.finRange 10) 10).map fun b => (a,b)

theorem allTypeMaps_mem (g : TypeMap) : g ∈ allTypeMaps := by
  apply List.mem_flatMap.mpr
  refine ⟨g.1,(functions_mem _ _ _).mpr (fun i => List.mem_finRange _),?_⟩
  exact List.mem_map.mpr ⟨g.2,(functions_mem _ _ _).mpr (fun i => List.mem_finRange _),rfl⟩

theorem allTypeMaps_nodup : allTypeMaps.Nodup := by
  apply List.pairwise_flatMap.mpr
  constructor
  · intro a _
    apply List.pairwise_map.mpr
    apply List.Pairwise.imp (l := functions (List.finRange 10) 10) _ (functions_nodup _ (by decide +kernel) _)
    intro b c h he
    exact h (congrArg Prod.snd he)
  · apply List.Pairwise.imp (l := functions (List.finRange 7) 7) _ (functions_nodup _ (by decide +kernel) _)
    intro a b h x hx y hy he
    obtain ⟨c,hc,rfl⟩ := List.mem_map.mp hx
    obtain ⟨d,hd,rfl⟩ := List.mem_map.mp hy
    exact h (congrArg Prod.fst he)

theorem allTypeMaps_length : allTypeMaps.length = 7^7*10^10 := by
  unfold allTypeMaps
  rw [flatMap_length_uniform _ _ (10^10)]
  · rw [functions_length]
    simp
  · intro a _
    rw [List.length_map,functions_length]
    simp

theorem allTypeMaps_count : (allTypeMaps.length : Rat) < 2^54 := by
  rw [allTypeMaps_length]
  decide +kernel

theorem identity_ne_reversal : identityMap ≠ reversalMap := by
  intro h
  have hh := congrFun (congrArg Prod.fst h) 0
  have hn : (id (0:Point)) ≠ reversePoint 0 := by decide +kernel
  exact hn hh

/-- beta raised to the source-score difference from its genuine maximum. -/
def relativeWeight (g : TypeMap) : Rat := 1/beta^((5066-score g.1 g.2).toNat)
def weightedTerm (g : TypeMap) : Rat := generalCoefficient g.1 g.2*relativeWeight g

def normalizedWeightedSum : Rat := (allTypeMaps.map weightedTerm).sum

theorem relativeWeight_positive (g : TypeMap) : 0 < relativeWeight g := reciprocal_beta_power_positive _

theorem relativeWeight_max (g : TypeMap) (h : score g.1 g.2 = 5066) : relativeWeight g = 1 := by
  simp [relativeWeight,h]
  decide +kernel

theorem reciprocal_antitone (a b : Rat) (ha : 0 < a) (hab : a ≤ b) : 1/b ≤ 1/a := by
  have hb : 0 < b := by grind only
  have hai : 0 ≤ a⁻¹ := by have h := Rat.inv_pos.mpr ha; grind only
  have haz : a ≠ 0 := by grind only
  have hc := Rat.mul_inv_cancel a haz
  have hm := Rat.mul_le_mul_of_nonneg_right hab hai
  have hbi : 0 ≤ b⁻¹ := by have h := Rat.inv_pos.mpr hb; grind only
  have hbz : b ≠ 0 := by grind only
  have hbc := Rat.mul_inv_cancel b hbz
  have hm2 := Rat.mul_le_mul_of_nonneg_right hm hbi
  rw [hc,Rat.one_mul] at hm2
  have he : b*a⁻¹*b⁻¹ = a⁻¹ := by
    rw [Rat.mul_comm b a⁻¹,Rat.mul_assoc,hbc,Rat.mul_one]
  rw [he] at hm2
  simpa only [Rat.div_def,Rat.one_mul] using hm2

theorem relativeWeight_lower_score (g : TypeMap) (h : score g.1 g.2 < 5066) : relativeWeight g ≤ 1/beta := by
  have hn : 1 ≤ (5066-score g.1 g.2).toNat := by omega
  let n := (5066-score g.1 g.2).toNat
  have hsucc : n = (n-1)+1 := by omega
  have hb : 1 ≤ beta := power_ge_one 2 (by decide +kernel) 564
  have hpow := power_ge_one beta hb (n-1)
  have hle : beta ≤ beta^n := by
    have hp : 0 ≤ beta := by have hh := beta_positive; grind only
    have hm := Rat.mul_le_mul_of_nonneg_right hpow hp
    rw [hsucc,Rat.pow_succ]
    grind only
  exact reciprocal_antitone beta (beta^n) beta_positive hle

theorem maximum_coefficient_support (g : TypeMap) (hmax : score g.1 g.2 = 5066)
    (hi : g ≠ identityMap) (hr : g ≠ reversalMap) : generalCoefficient g.1 g.2 = 0 := by
  obtain ⟨ha,hb⟩ := (score_max_iff g.1 g.2).mp hmax
  apply generalCoefficient_non_incidence
  intro he
  rcases stable_endomorphisms_exact _ _ ha hb he with hid | hrev
  · apply hi
    exact Prod.ext hid.1 hid.2
  · apply hr
    exact Prod.ext hrev.1 hrev.2

/-- Every non-orbit term has an explicit upper bound; no remainder is assumed. -/
theorem non_orbit_term_bound (g : TypeMap) (hi : g ≠ identityMap) (hr : g ≠ reversalMap) :
    weightedTerm g ≤ 2^450/beta := by
  by_cases hm : score g.1 g.2 = 5066
  · rw [weightedTerm,maximum_coefficient_support g hm hi hr,Rat.zero_mul]
    have h : 0 < (2^450/beta:Rat) := Rat.mul_pos (by decide +kernel) (Rat.inv_pos.mpr beta_positive)
    grind only
  · have hs := score_le_max g.1 g.2
    have hlt : score g.1 g.2 < 5066 := by omega
    have hw := relativeWeight_lower_score g hlt
    have hp : 0 ≤ relativeWeight g := by have h := relativeWeight_positive g; grind only
    have hc := (generalCoefficient_bounds g.1 g.2).2
    have h1 := Rat.mul_le_mul_of_nonneg_right hc hp
    have h2 := Rat.mul_le_mul_of_nonneg_left hw (by decide +kernel : (0:Rat) ≤ 2^450)
    unfold weightedTerm
    grind only

theorem rat_sum_single (xs : List α) (f : α → Rat) (s : α)
    (hn : xs.Nodup) (hs : s ∈ xs) (hz : ∀ x ∈ xs, x ≠ s → f x = 0) : (xs.map f).sum = f s := by
  induction xs with
  | nil => simp at hs
  | cons x xs ih =>
    have hn' := List.nodup_cons.mp hn
    simp only [List.mem_cons] at hs
    simp only [List.map_cons,List.sum_cons]
    rcases hs with he | ht
    · subst x
      have hzero : (xs.map f).sum = 0 := rat_sum_zero xs f (by
        intro y hy
        apply hz y (by simp [hy])
        intro h; subst y; exact hn'.1 hy)
      rw [hzero,Rat.add_zero]
    · have hxs : x ≠ s := by intro h; subst x; exact hn'.1 ht
      rw [hz x (by simp) hxs,ih hn'.2 ht (fun y hy => hz y (by simp [hy])),Rat.zero_add]

noncomputable def remainderTerm (g : TypeMap) : Rat :=
  if g = identityMap ∨ g = reversalMap then 0 else weightedTerm g
noncomputable def finiteRemainder : Rat := (allTypeMaps.map remainderTerm).sum

theorem finiteRemainder_bound : finiteRemainder < 1/2^60 := by
  have hp' : 0 < (2^450/beta:Rat) := Rat.mul_pos (by decide +kernel) (Rat.inv_pos.mpr beta_positive)
  have hp : 0 ≤ (2^450/beta:Rat) := by grind only
  have hterm (g : TypeMap) : remainderTerm g ≤ 2^450/beta := by
    unfold remainderTerm
    split
    · exact hp
    · rename_i h
      exact non_orbit_term_bound g (fun hi => h (Or.inl hi)) (fun hr => h (Or.inr hr))
  have hs := rat_sum_le allTypeMaps remainderTerm (fun _ => 2^450/beta) (fun g _ => hterm g)
  rw [rat_sum_const] at hs
  have hc := Rat.mul_lt_mul_of_pos_right allTypeMaps_count hp'
  have he : (2^54:Rat)*(2^450/beta) = 1/2^60 := by decide +kernel
  unfold finiteRemainder
  rw [he] at hc
  exact Std.lt_of_le_of_lt hs hc

theorem normalizedWeightedSum_split : normalizedWeightedSum =
    generalCoefficient id id+generalCoefficient reversePoint reverseFace+finiteRemainder := by
  let f1 := fun g : TypeMap => if g = identityMap then weightedTerm g else 0
  let fr := fun g : TypeMap => if g = reversalMap then weightedTerm g else 0
  have hs (g : TypeMap) : weightedTerm g = f1 g+fr g+remainderTerm g := by
    unfold f1 fr remainderTerm
    by_cases hi : g = identityMap <;> by_cases hr : g = reversalMap <;>
      simp [hi,hr,identity_ne_reversal,Ne.symm identity_ne_reversal] <;> try grind only
  have h1 := rat_sum_single allTypeMaps f1 identityMap allTypeMaps_nodup (allTypeMaps_mem _) (by intro g _ h; simp [f1,h])
  have hr := rat_sum_single allTypeMaps fr reversalMap allTypeMaps_nodup (allTypeMaps_mem _) (by intro g _ h; simp [fr,h])
  unfold normalizedWeightedSum
  have he : weightedTerm = (fun g => f1 g+fr g+remainderTerm g) := funext hs
  rw [he,rat_sum_add,rat_sum_add,h1,hr]
  have wi : relativeWeight identityMap = 1 := relativeWeight_max _ score_identity
  have wr : relativeWeight reversalMap = 1 := relativeWeight_max _ score_reversal
  simp only [f1,fr,ite_true,weightedTerm,wi,wr,Rat.mul_one]
  rfl

/-- Strict negativity from the actual full stochastic coefficients and the literal finite score. -/
theorem normalizedWeightedSum_negative : normalizedWeightedSum < -(1/2^60:Rat) := by
  rw [normalizedWeightedSum_split,general_signed_orbit]
  have h := finiteRemainder_bound
  have he : (1/2^59:Rat) = 2*(1/2^60) := by decide +kernel
  rw [he]
  grind only

end T7Weighted
