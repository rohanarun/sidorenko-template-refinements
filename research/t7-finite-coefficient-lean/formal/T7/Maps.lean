import T7.Finite
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7

def candidate (b0 b1 b2 b4 b5 b6 : Bool) : Point → Point
  | ⟨0,_⟩ => if b0 then 6 else 0
  | ⟨1,_⟩ => if b1 then 5 else 1
  | ⟨2,_⟩ => if b2 then 4 else 2
  | ⟨3,_⟩ => 3
  | ⟨4,_⟩ => if b4 then 4 else 2
  | ⟨5,_⟩ => if b5 then 5 else 1
  | ⟨6,_⟩ => if b6 then 6 else 0

def StablePoints (a : Point → Point) : Prop := ∀ p, pointColor (a p) = pointColor p
def StableFaces (b : Face → Face) : Prop := ∀ j, faceColor (b j) = faceColor j
def IncidenceEndomorphism (a : Point → Point) (b : Face → Face) : Prop :=
  ∀ p j, incident p j = true → incident (a p) (b j) = true
def HasExtension (a : Point → Point) : Prop := ∀ j : Face, ∃ k : Face,
  faceColor k = faceColor j ∧ ∀ p : Point, incident p j = true → incident (a p) k = true

instance (a : Point → Point) : Decidable (HasExtension a) := inferInstanceAs
  (Decidable (∀ j : Face, ∃ k : Face,
    faceColor k = faceColor j ∧ ∀ p : Point, incident p j = true → incident (a p) k = true))

theorem candidate_classification : ∀ b0 b1 b2 b4 b5 b6 : Bool,
  HasExtension (candidate b0 b1 b2 b4 b5 b6) →
    (∀ p, candidate b0 b1 b2 b4 b5 b6 p = p) ∨
    (∀ p, candidate b0 b1 b2 b4 b5 b6 p = reversePoint p) := by decide +kernel

theorem candidate_representation (a : Point → Point) (h : StablePoints a) :
    a = candidate (a 0 == 6) (a 1 == 5) (a 2 == 4)
      (a 4 == 4) (a 5 == 5) (a 6 == 6) := by
  funext i
  have all : ∀ i : Point, i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by decide +kernel
  have hi := all i
  rcases hi with rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · have rule : ∀ x : Point, pointColor x = pointColor (0 : Point) → x = (if x == 6 then 6 else 0) := by decide +kernel
    exact rule (a 0) (h 0)
  · have rule : ∀ x : Point, pointColor x = pointColor (1 : Point) → x = (if x == 5 then 5 else 1) := by decide +kernel
    exact rule (a 1) (h 1)
  · have rule : ∀ x : Point, pointColor x = pointColor (2 : Point) → x = (if x == 4 then 4 else 2) := by decide +kernel
    exact rule (a 2) (h 2)
  · have rule : ∀ x : Point, pointColor x = pointColor (3 : Point) → x = 3 := by decide +kernel
    exact rule (a 3) (h 3)
  · have rule : ∀ x : Point, pointColor x = pointColor (4 : Point) → x = (if x == 4 then 4 else 2) := by decide +kernel
    exact rule (a 4) (h 4)
  · have rule : ∀ x : Point, pointColor x = pointColor (5 : Point) → x = (if x == 5 then 5 else 1) := by decide +kernel
    exact rule (a 5) (h 5)
  · have rule : ∀ x : Point, pointColor x = pointColor (6 : Point) → x = (if x == 6 then 6 else 0) := by decide +kernel
    exact rule (a 6) (h 6)

theorem stable_points_classified (a : Point → Point)
    (h : StablePoints a) (he : HasExtension a) :
    a = id ∨ a = reversePoint := by
  rw [candidate_representation a h] at he ⊢
  rcases candidate_classification _ _ _ _ _ _ he with hi | hr
  · exact Or.inl (funext hi)
  · exact Or.inr (funext hr)

theorem identity_face_unique : ∀ j k : Face,
  (∀ p : Point, incident p j = true → incident p k = true) → k = j := by decide +kernel

theorem reversal_face_unique : ∀ j k : Face,
  (∀ p : Point, incident p j = true → incident (reversePoint p) k = true) →
  k = reverseFace j := by decide +kernel

theorem stable_endomorphisms_exact (a : Point → Point) (b : Face → Face)
    (ha : StablePoints a) (hb : StableFaces b) (he : IncidenceEndomorphism a b) :
    (a = id ∧ b = id) ∨ (a = reversePoint ∧ b = reverseFace) := by
  have hx : HasExtension a := fun j => ⟨b j, hb j, fun p hp => he p j hp⟩
  rcases stable_points_classified a ha hx with hi | hr
  · left
    refine ⟨hi, ?_⟩
    funext j
    apply identity_face_unique j (b j)
    simpa [hi] using fun p hp => he p j hp
  · right
    refine ⟨hr, ?_⟩
    funext j
    apply reversal_face_unique j (b j)
    simpa [hr] using fun p hp => he p j hp

theorem identity_is_stable_endomorphism : StablePoints id ∧ StableFaces id ∧
    IncidenceEndomorphism id id := by
  exact ⟨fun _ => rfl, fun _ => rfl, fun _ _ h => h⟩
theorem reversal_is_stable_endomorphism : StablePoints reversePoint ∧ StableFaces reverseFace ∧
    IncidenceEndomorphism reversePoint reverseFace := by
  refine ⟨?_, ?_, ?_⟩
  · unfold StablePoints; decide +kernel
  · unfold StableFaces; decide +kernel
  · intro p j h; rw [reversal_incidence]; exact h

def allPointMaps : List (List Point) := [false,true].flatMap fun b0 =>
  [false,true].flatMap fun b1 => [false,true].flatMap fun b2 =>
  [false,true].flatMap fun b4 => [false,true].flatMap fun b5 =>
  [false,true].map fun b6 => List.ofFn (candidate b0 b1 b2 b4 b5 b6)

theorem enumeration_size : allPointMaps.length = 64 := by decide +kernel
theorem enumeration_unique : allPointMaps.Nodup := by decide +kernel
theorem noninjective_count : (allPointMaps.filter fun l => !decide l.Nodup).length = 56 := by decide +kernel

end T7
