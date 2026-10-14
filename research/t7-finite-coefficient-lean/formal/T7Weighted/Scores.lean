import T7Gap
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Weighted
open T7 T7Gap

def pointLoss (p q : Point) : Int := 37*((degree q : Int)-(degree p : Int))^2

def faceScore (a : Point → Point) (j k : Face) : Int :=
  ((face j).map fun p => 2*(faceHistogram k (degree (a p)) : Int)).sum - (faceNorm k : Int)

/-- The literal source Q after collecting incidence terms by their source point and face. -/
def score (a : Point → Point) (b : Face → Face) : Int :=
  5032 - ((List.finRange 7).map fun p => pointLoss p (a p)).sum +
    ((List.finRange 10).map fun j => faceScore a j (b j)).sum

/-- Source Q before regrouping: point and face prior exponents plus all thirty pair scores. -/
def sourceScore (a : Point → Point) (b : Face → Face) : Int :=
  -((List.finRange 7).map fun p => (37:Int)*(degree (a p):Int)^2).sum -
  (((List.finRange 10).map fun j => (faceNorm (b j) : Int)).sum) +
  ((List.finRange 30).map fun c => (pairScore (a (corner c).1) (b (corner c).2) : Int)).sum

theorem pointLoss_nonneg : ∀ p q, 0 ≤ pointLoss p q := by decide +kernel

theorem pointLoss_zero_iff : ∀ p q, pointLoss p q = 0 ↔ degree q = degree p := by decide +kernel

theorem pointLoss_gap : ∀ p q, degree q ≠ degree p → 37 ≤ pointLoss p q := by decide +kernel

theorem int_sum_nonneg (xs : List α) (f : α → Int) (h : ∀ x ∈ xs, 0 ≤ f x) : 0 ≤ (xs.map f).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    have hx := h x (by simp)
    have ht := ih (fun y hy => h y (by simp [hy]))
    simp only [List.map_cons,List.sum_cons]
    grind only

theorem int_sum_le (xs : List α) (f g : α → Int) (h : ∀ x ∈ xs, f x ≤ g x) :
    (xs.map f).sum ≤ (xs.map g).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    have hx := h x (by simp)
    have ht := ih (fun y hy => h y (by simp [hy]))
    simp only [List.map_cons,List.sum_cons]
    grind only

theorem int_member_le_sum (xs : List α) (f : α → Int) (h : ∀ x ∈ xs, 0 ≤ f x)
    (x : α) (hx : x ∈ xs) : f x ≤ (xs.map f).sum := by
  induction xs with
  | nil => simp at hx
  | cons y ys ih =>
    have hy := h y (by simp)
    have ht : ∀ z ∈ ys, 0 ≤ f z := fun z hz => h z (by simp [hz])
    have hs := int_sum_nonneg ys f ht
    simp only [List.map_cons,List.sum_cons]
    rcases List.mem_cons.mp hx with he | he
    · subst x; grind only
    · have hh := ih ht he; grind only

theorem face_length : ∀ j, (face j).length = 3 := by decide +kernel

def faceFirst (j : Face) : Point := (face j)[0]'(by rw [face_length]; decide)
def faceSecond (j : Face) : Point := (face j)[1]'(by rw [face_length]; decide)
def faceThird (j : Face) : Point := (face j)[2]'(by rw [face_length]; decide)

theorem face_triple : ∀ j, face j = [faceFirst j,faceSecond j,faceThird j] := by decide +kernel

theorem three_image_face_bound : ∀ p q r : Point, ∀ k : Face,
    2*(faceHistogram k (degree p) : Int)+2*(faceHistogram k (degree q) : Int)+
    2*(faceHistogram k (degree r) : Int)-(faceNorm k : Int) ≤ 7 := by decide +kernel

theorem faceScore_le_seven (a : Point → Point) (j k : Face) : faceScore a j k ≤ 7 := by
  unfold faceScore
  rw [face_triple]
  simp only [List.map_cons,List.map_nil,List.sum_cons,List.sum_nil]
  have h := three_image_face_bound (a (faceFirst j)) (a (faceSecond j)) (a (faceThird j)) k
  grind only

theorem stable_faceScore_table : ∀ j k,
    faceScore id j k ≤ (faceNorm j : Int) ∧
    (faceScore id j k = (faceNorm j : Int) ↔ faceColor k = faceColor j) := by decide +kernel

theorem face_norm_total : ((List.finRange 10).map fun j => (faceNorm j : Int)).sum = 34 := by decide +kernel

theorem stable_faceScore (a : Point → Point) (h : ∀ p, degree (a p) = degree p) (j k : Face) :
    faceScore a j k = faceScore id j k := by
  unfold faceScore
  congr 1
  congr 1
  apply List.map_congr_left
  intro p _
  rw [h]
  rfl

theorem stable_points_degree (a : Point → Point) : StablePoints a ↔ ∀ p, degree (a p) = degree p := by
  exact forall_congr' (fun p => point_cells_by_degree (a p) p)

theorem score_point_mismatch (a : Point → Point) (b : Face → Face)
    (h : ¬ StablePoints a) : score a b ≤ 5065 := by
  have hw : ∃ p, degree (a p) ≠ degree p := by
    apply Classical.byContradiction
    intro hn
    apply h
    apply (stable_points_degree a).mpr
    intro p
    apply Classical.byContradiction
    intro hp
    exact hn ⟨p,hp⟩
  obtain ⟨p,hp⟩ := hw
  have hpoint := int_member_le_sum (List.finRange 7) (fun p => pointLoss p (a p))
    (fun p _ => pointLoss_nonneg p (a p)) p (List.mem_finRange p)
  have hgap := pointLoss_gap p (a p) hp
  have hface := int_sum_le (List.finRange 10) (fun j => faceScore a j (b j)) (fun _ => 7)
    (fun j _ => faceScore_le_seven a j (b j))
  have htotal : ((List.finRange 10).map fun _ => (7:Int)).sum = 70 := by decide +kernel
  rw [htotal] at hface
  unfold score
  grind only

def faceDefect (j k : Face) : Int := (faceNorm j : Int)-faceScore id j k

theorem faceDefect_nonneg (j k : Face) : 0 ≤ faceDefect j k := by
  have h := (stable_faceScore_table j k).1
  unfold faceDefect
  grind only

theorem faceDefect_zero_iff (j k : Face) : faceDefect j k = 0 ↔ faceColor k = faceColor j := by
  have h := (stable_faceScore_table j k).2
  unfold faceDefect
  grind only

theorem int_sum_sub (xs : List α) (f g : α → Int) :
    (xs.map fun x => f x-g x).sum = (xs.map f).sum-(xs.map g).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp only [List.map_cons,List.sum_cons,ih]; grind only

theorem score_stable_exact (a : Point → Point) (b : Face → Face) (ha : StablePoints a) :
    score a b = 5066-((List.finRange 10).map fun j => faceDefect j (b j)).sum := by
  have hd := (stable_points_degree a).mp ha
  have hzero : ((List.finRange 7).map fun p => pointLoss p (a p)).sum = 0 := by
    apply T7.sum_zero
    intro p _
    exact (pointLoss_zero_iff p (a p)).mpr (hd p)
  unfold score faceDefect
  rw [hzero,int_sum_sub,face_norm_total]
  simp only [stable_faceScore a hd]
  grind only

theorem score_le_max (a : Point → Point) (b : Face → Face) : score a b ≤ 5066 := by
  by_cases ha : StablePoints a
  · rw [score_stable_exact a b ha]
    have h := int_sum_nonneg (List.finRange 10) (fun j => faceDefect j (b j)) (fun j _ => faceDefect_nonneg j (b j))
    grind only
  · have h := score_point_mismatch a b ha
    grind only

/-- Only the literal stable-color-preserving maps attain the maximum source score. -/
theorem score_max_iff (a : Point → Point) (b : Face → Face) :
    score a b = 5066 ↔ StablePoints a ∧ StableFaces b := by
  constructor
  · intro he
    have ha : StablePoints a := by
      apply Classical.byContradiction
      intro hn
      have h := score_point_mismatch a b hn
      grind only
    refine ⟨ha,?_⟩
    rw [score_stable_exact a b ha] at he
    intro j
    have h := int_member_le_sum (List.finRange 10) (fun j => faceDefect j (b j))
      (fun j _ => faceDefect_nonneg j (b j)) j (List.mem_finRange j)
    have hn := faceDefect_nonneg j (b j)
    apply (faceDefect_zero_iff j (b j)).mp
    grind only
  · rintro ⟨ha,hb⟩
    rw [score_stable_exact a b ha]
    have hz : ((List.finRange 10).map fun j => faceDefect j (b j)).sum = 0 := by
      apply T7.sum_zero
      intro j _
      exact (faceDefect_zero_iff j (b j)).mpr (hb j)
    rw [hz]
    grind only

theorem score_identity : score id id = 5066 := (score_max_iff _ _).mpr
  ⟨identity_is_stable_endomorphism.1,identity_is_stable_endomorphism.2.1⟩

theorem score_reversal : score reversePoint reverseFace = 5066 := (score_max_iff _ _).mpr
  ⟨reversal_is_stable_endomorphism.1,reversal_is_stable_endomorphism.2.1⟩

end T7Weighted
