import T7Gap.ThinningLaw
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

/-- Source feature at any type pair. The nonincident pair uses the empty activity set. -/
def pairFeature (p : Point) (j : Face) (a : Mask) (o : ActivationOutcome) : Rat :=
  if incident p j then phi (cornerIndex p j) a o else if IsZero a then 1 else 0

def pairMoment (p : Point) (j : Face) (a b : Mask) : Rat :=
  (activationLaw (cornerIndex p j)).mean (fun o => pairFeature p j a o*pairFeature p j b o)

theorem pairMoment_incident (p : Point) (j : Face) (h : incident p j = true) (a b : Mask) :
    pairMoment p j a b = activationMoment (cornerIndex p j) a b := by
  simp only [pairMoment,pairFeature,h,ite_true,activationMoment]

theorem pairMoment_nonincident (p : Point) (j : Face) (h : incident p j = false)
    (a b : Mask) (ha : NonemptyMask a) : pairMoment p j a b = 0 := by
  have hne : ¬ IsZero a := by
    obtain ⟨c,hc⟩ := ha
    intro hz
    have ht := hz c
    rw [hc] at ht
    contradiction
  simp [pairMoment,pairFeature,h,hne,FiniteLaw.mean_const]

def generalCoefficient (a : Point → Point) (b : Face → Face) : Rat :=
  (allLabelings.map fun labels => ((List.finRange 30).map fun c =>
    pairMoment (a (corner c).1) (b (corner c).2)
      (labels (leftEdge c)) (labels (rightEdge c))).prod).sum

theorem rat_prod_zero (xs : List Rat) (h : 0 ∈ xs) : xs.prod = 0 := by
  induction xs with
  | nil => simp at h
  | cons x xs ih =>
    rcases List.mem_cons.mp h with hx | ht
    · rw [← hx,List.prod_cons,Rat.zero_mul]
    · rw [List.prod_cons,ih ht,Rat.mul_zero]

theorem rat_sum_zero (xs : List α) (f : α → Rat) (h : ∀ x ∈ xs, f x = 0) : (xs.map f).sum = 0 := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    simp only [List.map_cons,List.sum_cons]
    rw [h x (by simp),ih (fun y hy => h y (by simp [hy])),Rat.zero_add]

/-- Vanishing for every non-incidence type map, including maps with repeated images. -/
theorem generalCoefficient_non_incidence (a : Point → Point) (b : Face → Face)
    (h : ¬ IncidenceEndomorphism a b) : generalCoefficient a b = 0 := by
  have hw : ∃ p j, incident p j = true ∧ incident (a p) (b j) = false := by
    apply Classical.byContradiction
    intro hn
    apply h
    intro p j hp
    have hne : ¬ incident (a p) (b j) = false := fun hb => hn ⟨p,j,hp,hb⟩
    cases he : incident (a p) (b j) <;> simp_all
  obtain ⟨p,j,hp,hbad⟩ := hw
  obtain ⟨c,hc⟩ := (corner_bijection.2 p j).mp hp
  unfold generalCoefficient
  apply rat_sum_zero
  intro labels hl
  apply rat_prod_zero
  apply List.mem_map.mpr
  refine ⟨c,List.mem_finRange _,?_⟩
  rw [hc]
  exact pairMoment_nonincident _ _ hbad _ _ ((labelings_mem labels).mp hl (leftEdge c))

theorem cornerIndex_corner : ∀ c, cornerIndex (corner c).1 (corner c).2 = c := by decide +kernel

theorem corners_incident : ∀ c, incident (corner c).1 (corner c).2 = true := by decide +kernel

theorem general_identity : generalCoefficient id id = stochasticCoefficient id := by
  unfold generalCoefficient stochasticCoefficient
  simp only [id_eq,pairMoment_incident _ _ (corners_incident _),cornerIndex_corner]

theorem general_reversal : generalCoefficient reversePoint reverseFace = stochasticCoefficient reverseCorner := by
  have hr (c : Corner) : pairMoment (reversePoint (corner c).1) (reverseFace (corner c).2) =
      activationMoment (reverseCorner c) := by
    have h := reversal_corner_meaning c
    have hi := corners_incident (reverseCorner c)
    rw [h] at hi
    funext x y
    rw [pairMoment_incident _ _ hi]
    have he : cornerIndex (reversePoint (corner c).1) (reverseFace (corner c).2) = reverseCorner c := by
      apply corner_bijection.1
      rw [cornerIndex_valid _ _ hi]
      exact h.symm
    rw [he]
  unfold generalCoefficient stochasticCoefficient
  simp only [hr]

theorem general_signed_orbit : generalCoefficient id id+generalCoefficient reversePoint reverseFace = -(1/2^59:Rat) := by
  rw [general_identity,general_reversal,stochastic_signed_orbit]

end T7Gap
