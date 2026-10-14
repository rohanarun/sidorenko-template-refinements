import T7.Maps
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7
abbrev Mask := Corner → Bool
abbrev Labeling := Edge → Mask
def leftEdge : Corner → Edge
  | ⟨0, _⟩ => 0
  | ⟨1, _⟩ => 0
  | ⟨2, _⟩ => 1
  | ⟨3, _⟩ => 0
  | ⟨4, _⟩ => 0
  | ⟨5, _⟩ => 2
  | ⟨6, _⟩ => 1
  | ⟨7, _⟩ => 1
  | ⟨8, _⟩ => 2
  | ⟨9, _⟩ => 3
  | ⟨10, _⟩ => 3
  | ⟨11, _⟩ => 5
  | ⟨12, _⟩ => 4
  | ⟨13, _⟩ => 4
  | ⟨14, _⟩ => 5
  | ⟨15, _⟩ => 6
  | ⟨16, _⟩ => 6
  | ⟨17, _⟩ => 8
  | ⟨18, _⟩ => 7
  | ⟨19, _⟩ => 7
  | ⟨20, _⟩ => 8
  | ⟨21, _⟩ => 9
  | ⟨22, _⟩ => 9
  | ⟨23, _⟩ => 11
  | ⟨24, _⟩ => 10
  | ⟨25, _⟩ => 10
  | ⟨26, _⟩ => 11
  | ⟨27, _⟩ => 12
  | ⟨28, _⟩ => 12
  | ⟨29, _⟩ => 13
  | ⟨n+30, h⟩ => by omega
def rightEdge : Corner → Edge
  | ⟨0, _⟩ => 1
  | ⟨1, _⟩ => 3
  | ⟨2, _⟩ => 3
  | ⟨3, _⟩ => 2
  | ⟨4, _⟩ => 4
  | ⟨5, _⟩ => 4
  | ⟨6, _⟩ => 2
  | ⟨7, _⟩ => 6
  | ⟨8, _⟩ => 6
  | ⟨9, _⟩ => 5
  | ⟨10, _⟩ => 7
  | ⟨11, _⟩ => 7
  | ⟨12, _⟩ => 5
  | ⟨13, _⟩ => 9
  | ⟨14, _⟩ => 9
  | ⟨15, _⟩ => 8
  | ⟨16, _⟩ => 10
  | ⟨17, _⟩ => 10
  | ⟨18, _⟩ => 8
  | ⟨19, _⟩ => 12
  | ⟨20, _⟩ => 12
  | ⟨21, _⟩ => 11
  | ⟨22, _⟩ => 13
  | ⟨23, _⟩ => 13
  | ⟨24, _⟩ => 11
  | ⟨25, _⟩ => 14
  | ⟨26, _⟩ => 14
  | ⟨27, _⟩ => 13
  | ⟨28, _⟩ => 14
  | ⟨29, _⟩ => 14
  | ⟨n+30, h⟩ => by omega

def support (e : Edge) (c : Corner) : Bool :=
  let (u,v) := pointEdge e
  let (p,j) := corner c
  ((p == u) || (p == v)) && incident u j && incident v j

def unionMask (a b : Mask) : Mask := fun c => a c || b c
def diffMask (a b : Mask) : Mask := fun c => xor (a c) (b c)
def M (c : Corner) : Mask := unionMask (support (leftEdge c)) (support (rightEdge c))
def D (c : Corner) : Mask := diffMask (support (leftEdge c)) (support (rightEdge c))
def SubsetMask (a b : Mask) : Prop := ∀ c, a c = true → b c = true
instance (a b : Mask) : Decidable (SubsetMask a b) := inferInstanceAs (Decidable (∀ c, a c = true → b c = true))
def NonemptyMask (a : Mask) : Prop := ∃ c, a c = true
instance (a : Mask) : Decidable (NonemptyMask a) := inferInstanceAs (Decidable (∃ c, a c = true))
def maskEq (a b : Mask) : Prop := ∀ c, a c = b c
instance (a b : Mask) : Decidable (maskEq a b) := inferInstanceAs (Decidable (∀ c, a c = b c))
def emptyMask : Mask := fun _ => false

theorem support_incidence : ∀ e c, support e c = true ↔ leftEdge c = e ∨ rightEdge c = e := by decide +kernel
theorem supports_intersect : ∀ c d,
  (support (leftEdge c) d = true ∧ support (rightEdge c) d = true) ↔ d = c := by decide +kernel
theorem support_intersection : ∀ e d,
    (∀ c, support e c = true → M c d = true) ↔ support e d = true := by decide +kernel
theorem support_sizes : ∀ e, ((List.finRange 30).filter (support e)).length = 4 := by decide +kernel
theorem law_sizes : ∀ c,
    ((List.finRange 30).filter (M c)).length = 7 ∧
    ((List.finRange 30).filter (D c)).length = 6 := by decide +kernel
theorem diff_subset_union : ∀ c, SubsetMask (D c) (M c) := by decide +kernel
theorem diff_nonempty : ∀ c, NonemptyMask (D c) := by decide +kernel

def sigma (c : Corner) : Int := if c == 0 then -1 else 1
/-- Four times formula (1) in the packet. All operations are exact integer operations. -/
def momentNumerator (c : Corner) (a b : Mask) : Int :=
  (if SubsetMask (unionMask a b) (M c) then
    (if maskEq (diffMask a b) emptyMask then 2 else 0) +
    (if maskEq (diffMask a b) (D c) then sigma c else 0) else 0) +
  (if SubsetMask (unionMask a b) (D c) then
    (if maskEq (diffMask a b) emptyMask then 2 else 0) -
    (if maskEq (diffMask a b) (D c) then sigma c else 0) else 0)
def moment (c : Corner) (a b : Mask) : Rat := (momentNumerator c a b : Rat) / 4

theorem canonical_moment : ∀ c,
    momentNumerator c (support (leftEdge c)) (support (rightEdge c)) = sigma c := by decide +kernel

def termNumerator (a : Labeling) : Int :=
  (List.finRange 30).map (fun c => momentNumerator c (a (leftEdge c)) (a (rightEdge c))) |>.prod
def term (a : Labeling) : Rat := (termNumerator a : Rat) / (4^30)

theorem canonical_product : term support = -(1 / 4^30 : Rat) := by decide +kernel

theorem canonical_numerator : termNumerator support = -1 := by decide +kernel

theorem moment_support (c : Corner) (a b : Mask)
    (h : momentNumerator c a b ≠ 0) : SubsetMask (unionMask a b) (M c) := by
  by_cases hM : SubsetMask (unionMask a b) (M c)
  · exact hM
  · have hD : ¬ SubsetMask (unionMask a b) (D c) := by
      intro hd
      apply hM
      intro d hq
      exact diff_subset_union c d (hd d hq)
    simp [momentNumerator, hM, hD] at h

theorem disjoint_moment_zero (c : Corner) (a b : Mask)
    (hne : NonemptyMask (unionMask a b))
    (hd : ∀ d, a d = true → b d = false) : momentNumerator c a b = 0 := by
  have hdiff : maskEq (diffMask a b) (unionMask a b) := by
    intro d
    have hh := hd d
    cases ha : a d <;> cases hb : b d <;> simp_all [diffMask, unionMask]
  have hnot : ¬ maskEq (diffMask a b) emptyMask := by
    intro hnil
    obtain ⟨d, hq⟩ := hne
    have hh := hnil d
    rw [hdiff d, hq] at hh
    contradiction
  by_cases he : maskEq (diffMask a b) (D c)
  · have hD : SubsetMask (unionMask a b) (D c) := by
      intro d hq
      rw [← he d, hdiff d]
      exact hq
    have hM : SubsetMask (unionMask a b) (M c) := by
      intro d hq
      exact diff_subset_union c d (hD d hq)
    simp [momentNumerator, hnot, he, hD, hM]
    omega
  · simp [momentNumerator, hnot, he]

theorem moment_overlap (c : Corner) (a b : Mask)
    (ha : NonemptyMask a) (hm : momentNumerator c a b ≠ 0) :
    ∃ d, a d = true ∧ b d = true := by
  by_cases hi : ∃ d, a d = true ∧ b d = true
  · exact hi
  · have hd : ∀ d, a d = true → b d = false := by
      intro d hda
      apply Bool.eq_false_iff.mpr
      intro hdb
      exact hi ⟨d, hda, hdb⟩
    have hn : NonemptyMask (unionMask a b) := by
      obtain ⟨d, hh⟩ := ha
      exact ⟨d, by simp [unionMask, hh]⟩
    exact False.elim (hm (disjoint_moment_zero c a b hn hd))

theorem factor_ne_zero (l : List Int) (hp : l.prod ≠ 0) (x : Int) (hx : x ∈ l) : x ≠ 0 := by
  intro hz
  induction l with
  | nil => simp at hx
  | cons y ys ih =>
    simp only [List.mem_cons] at hx
    rcases hx with he | ht
    · have hy : y = 0 := by omega
      simp [hy] at hp
    · apply ih (fun h => hp (by simp [h])) ht

theorem term_factors_nonzero (a : Labeling) (h : termNumerator a ≠ 0) (c : Corner) :
    momentNumerator c (a (leftEdge c)) (a (rightEdge c)) ≠ 0 := by
  apply factor_ne_zero _ h
  exact List.mem_map.mpr ⟨c, List.mem_finRange c, rfl⟩

theorem term_support (a : Labeling) (h : termNumerator a ≠ 0) :
    ∀ e, SubsetMask (a e) (support e) := by
  intro e d hed
  apply (support_intersection e d).mp
  intro c hc
  have hm := moment_support c (a (leftEdge c)) (a (rightEdge c)) (term_factors_nonzero a h c)
  apply hm d
  rcases (support_incidence e c).mp hc with hl | hr
  · simp [unionMask, hl, hed]
  · simp [unionMask, hr, hed]

/-- Pointwise uniqueness for the full coefficient, without enumerating its huge index set. -/
theorem nonzero_labeling_unique (a : Labeling) (hne : ∀ e, NonemptyMask (a e))
    (h : termNumerator a ≠ 0) : a = support := by
  have hs := term_support a h
  funext e d
  cases had : a e d <;> cases hud : support e d
  · rfl
  · have hec := (support_incidence e d).mp hud
    obtain ⟨x, hxl, hxr⟩ := moment_overlap d (a (leftEdge d)) (a (rightEdge d))
      (hne _) (term_factors_nonzero a h d)
    have hxd : x = d := (supports_intersect d x).mp ⟨hs _ _ hxl, hs _ _ hxr⟩
    subst x
    rcases hec with hl | hr
    · rw [hl, had] at hxl; contradiction
    · rw [hr, had] at hxr; contradiction
  · have := hs e d had
    rw [hud] at this
    contradiction
  · rfl

theorem noncanonical_term_zero (a : Labeling) (hne : ∀ e, NonemptyMask (a e))
    (h : a ≠ support) : termNumerator a = 0 := by
  by_cases hz : termNumerator a = 0
  · exact hz
  · exact False.elim (h (nonzero_labeling_unique a hne hz))

end T7
