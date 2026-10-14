import T7.Enumeration
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7
def reverseCorner : Fin 30 → Corner
  | ⟨0, _⟩ => 29
  | ⟨1, _⟩ => 28
  | ⟨2, _⟩ => 27
  | ⟨3, _⟩ => 26
  | ⟨4, _⟩ => 25
  | ⟨5, _⟩ => 24
  | ⟨6, _⟩ => 23
  | ⟨7, _⟩ => 22
  | ⟨8, _⟩ => 21
  | ⟨9, _⟩ => 20
  | ⟨10, _⟩ => 19
  | ⟨11, _⟩ => 18
  | ⟨12, _⟩ => 17
  | ⟨13, _⟩ => 16
  | ⟨14, _⟩ => 15
  | ⟨15, _⟩ => 14
  | ⟨16, _⟩ => 13
  | ⟨17, _⟩ => 12
  | ⟨18, _⟩ => 11
  | ⟨19, _⟩ => 10
  | ⟨20, _⟩ => 9
  | ⟨21, _⟩ => 8
  | ⟨22, _⟩ => 7
  | ⟨23, _⟩ => 6
  | ⟨24, _⟩ => 5
  | ⟨25, _⟩ => 4
  | ⟨26, _⟩ => 3
  | ⟨27, _⟩ => 2
  | ⟨28, _⟩ => 1
  | ⟨29, _⟩ => 0
  | ⟨n+30, h⟩ => by omega
def reverseEdge : Fin 15 → Edge
  | ⟨0, _⟩ => 14
  | ⟨1, _⟩ => 13
  | ⟨2, _⟩ => 11
  | ⟨3, _⟩ => 12
  | ⟨4, _⟩ => 10
  | ⟨5, _⟩ => 8
  | ⟨6, _⟩ => 9
  | ⟨7, _⟩ => 7
  | ⟨8, _⟩ => 5
  | ⟨9, _⟩ => 6
  | ⟨10, _⟩ => 4
  | ⟨11, _⟩ => 2
  | ⟨12, _⟩ => 3
  | ⟨13, _⟩ => 1
  | ⟨14, _⟩ => 0

theorem reversal_corner_meaning : ∀ c, corner (reverseCorner c) =
    (reversePoint (corner c).1, reverseFace (corner c).2) := by decide +kernel
theorem reversal_edge_meaning : ∀ e, pointEdge (reverseEdge e) =
    (reversePoint (pointEdge e).2, reversePoint (pointEdge e).1) := by decide +kernel
theorem reverse_edge_involution : ∀ e, reverseEdge (reverseEdge e) = e := by decide +kernel
theorem reverse_corner_permutation : ((List.finRange 30).map reverseCorner).Perm
    (List.finRange 30) := by decide +kernel
theorem reverse_local_edges : ∀ c,
  (reverseEdge (leftEdge (reverseCorner c)) = leftEdge c ∧
   reverseEdge (rightEdge (reverseCorner c)) = rightEdge c) ∨
  (reverseEdge (leftEdge (reverseCorner c)) = rightEdge c ∧
   reverseEdge (rightEdge (reverseCorner c)) = leftEdge c) := by decide +kernel

theorem moment_symmetric (c : Corner) (a b : Mask) :
    momentNumerator c a b = momentNumerator c b a := by
  have hu : unionMask a b = unionMask b a := by
    funext d; unfold unionMask; cases a d <;> cases b d <;> rfl
  have hd : diffMask a b = diffMask b a := by
    funext d; unfold diffMask; cases a d <;> cases b d <;> rfl
  unfold momentNumerator
  rw [hu, hd]

theorem perm_int_prod {l k : List Int} (h : l.Perm k) : l.prod = k.prod := by
  induction h with
  | nil => rfl
  | cons a h ih => simp only [List.prod_cons, ih]
  | swap a b l => simp only [List.prod_cons]; grind
  | trans h1 h2 ih1 ih2 => exact ih1.trans ih2

def relabel (a : Labeling) : Labeling := fun e => a (reverseEdge e)
def reverseCanonical : Labeling := relabel support
def reverseTermNumerator (a : Labeling) : Int :=
  ((List.finRange 30).map fun c =>
    momentNumerator (reverseCorner c) (a (leftEdge c)) (a (rightEdge c))).prod

theorem reverse_term_reindex (a : Labeling) : reverseTermNumerator a = termNumerator (relabel a) := by
  let g := fun c => momentNumerator c ((relabel a) (leftEdge c)) ((relabel a) (rightEdge c))
  have hh : (fun c => momentNumerator (reverseCorner c) (a (leftEdge c)) (a (rightEdge c))) =
      g ∘ reverseCorner := by
    funext c
    rcases reverse_local_edges c with h | h
    · simp only [Function.comp_def, g, relabel, h.1, h.2]
    · simp only [Function.comp_def, g, relabel, h.1, h.2]
      exact moment_symmetric _ _ _
  unfold reverseTermNumerator termNumerator
  rw [hh, ← List.map_map]
  exact perm_int_prod (reverse_corner_permutation.map g)

theorem relabel_involution (a : Labeling) : relabel (relabel a) = a := by
  funext e; simp only [relabel, reverse_edge_involution]

theorem reverse_nonzero_unique (a : Labeling) (hne : ∀ e, NonemptyMask (a e))
    (h : reverseTermNumerator a ≠ 0) : a = reverseCanonical := by
  rw [reverse_term_reindex] at h
  have hi := nonzero_labeling_unique (relabel a) (fun e => hne _) h
  have hh := congrArg relabel hi
  rw [relabel_involution] at hh
  exact hh

theorem reverse_canonical_numerator : reverseTermNumerator reverseCanonical = -1 := by
  rw [reverse_term_reindex]
  unfold reverseCanonical
  rw [relabel_involution]
  exact canonical_numerator

def reverseFullCoefficient : Rat := ((allLabelings.map reverseTermNumerator).sum : Rat) / 4^30

theorem reverse_full_numerator : (allLabelings.map reverseTermNumerator).sum = -1 := by
  rw [sum_single allLabelings reverseTermNumerator reverseCanonical labelings_nodup
    ((labelings_mem reverseCanonical).mpr (fun e => support_nonempty _))]
  · exact reverse_canonical_numerator
  · intro a ha hn
    by_cases hz : reverseTermNumerator a = 0
    · exact hz
    · exact False.elim (hn (reverse_nonzero_unique a ((labelings_mem a).mp ha) hz))

theorem reverse_full_coefficient_exact : reverseFullCoefficient = -(1 / 4^30 : Rat) := by
  unfold reverseFullCoefficient
  rw [reverse_full_numerator]
  decide +kernel

theorem signed_orbit_coefficient : fullCoefficient + reverseFullCoefficient = -(1 / 2^59 : Rat) := by
  rw [full_coefficient_exact, reverse_full_coefficient_exact]
  decide +kernel
end T7
