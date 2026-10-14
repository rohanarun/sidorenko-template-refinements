import T7.Maps
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7

structure GraphAutomorphism where
  toFun : Vertex → Vertex
  invFun : Vertex → Vertex
  left_inv : ∀ v, invFun (toFun v) = v
  right_inv : ∀ v, toFun (invFun v) = v
  preserves : ∀ u v, adjacent (toFun u) (toFun v) = adjacent u v

theorem vertices_complete (v : Vertex) : v ∈ vertices := by
  cases v with
  | inl p => simp [vertices, List.mem_finRange]
  | inr j => simp [vertices, List.mem_finRange]

theorem automorphism_perm (f : GraphAutomorphism) : (vertices.map f.toFun).Perm vertices := by
  have hinj : ∀ u v, f.toFun u = f.toFun v → u = v := by
    intro u v h
    have hh := congrArg f.invFun h
    simpa [f.left_inv] using hh
  have hn : (vertices.map f.toFun).Nodup := by
    apply List.pairwise_map.mpr
    exact List.Pairwise.imp (fun {a b} hn he => hn (hinj a b he)) vertices_nodup
  apply (List.perm_ext_iff_of_nodup hn vertices_nodup).mpr
  intro v
  constructor
  · intro _; exact vertices_complete v
  · intro _; exact List.mem_map.mpr ⟨f.invFun v, vertices_complete _, f.right_inv v⟩

theorem automorphism_count (f : GraphAutomorphism) (p q : Vertex → Bool)
    (h : ∀ v, p (f.toFun v) = q v) :
    (vertices.filter p).length = (vertices.filter q).length := by
  have hp := ((automorphism_perm f).filter p).length_eq
  rw [List.filter_map, List.length_map] at hp
  have he : p ∘ f.toFun = q := funext h
  rw [he] at hp
  exact hp.symm

def graphDegree (v : Vertex) : Nat := (vertices.filter (adjacent v)).length

theorem automorphism_degree (f : GraphAutomorphism) (v : Vertex) :
    graphDegree (f.toFun v) = graphDegree v :=
  automorphism_count f _ _ (fun w => f.preserves v w)

def neighborDegreeCount (v : Vertex) (d : Nat) : Nat :=
  (vertices.filter fun w => adjacent v w && (graphDegree w == d)).length

theorem automorphism_neighbor_degree (f : GraphAutomorphism) (v : Vertex) (d : Nat) :
    neighborDegreeCount (f.toFun v) d = neighborDegreeCount v d := by
  apply automorphism_count f
  intro w
  simp only [f.preserves, automorphism_degree]

def graphColor : Vertex → Nat
  | .inl p => pointColor p
  | .inr j => 4 + faceColor j

def graphSignature (v : Vertex) : Nat × List Nat :=
  (graphDegree v, (List.range 7).map (neighborDegreeCount v))

theorem signature_color : ∀ u v : Vertex,
    graphSignature u = graphSignature v → graphColor u = graphColor v := by
  intro u v
  cases u with
  | inl p => cases v with
    | inl q => exact (by decide +kernel : ∀ p q : Point, graphSignature (.inl p) = graphSignature (.inl q) → graphColor (.inl p) = graphColor (.inl q)) p q
    | inr k => exact (by decide +kernel : ∀ p : Point, ∀ k : Face, graphSignature (.inl p) = graphSignature (.inr k) → graphColor (.inl p) = graphColor (.inr k)) p k
  | inr j => cases v with
    | inl q => exact (by decide +kernel : ∀ j : Face, ∀ q : Point, graphSignature (.inr j) = graphSignature (.inl q) → graphColor (.inr j) = graphColor (.inl q)) j q
    | inr k => exact (by decide +kernel : ∀ j k : Face, graphSignature (.inr j) = graphSignature (.inr k) → graphColor (.inr j) = graphColor (.inr k)) j k

theorem automorphism_color (f : GraphAutomorphism) (v : Vertex) :
    graphColor (f.toFun v) = graphColor v := by
  apply signature_color
  unfold graphSignature
  rw [automorphism_degree]
  have hh : neighborDegreeCount (f.toFun v) = neighborDegreeCount v :=
    funext (automorphism_neighbor_degree f v)
  rw [hh]

def autoPoint (f : GraphAutomorphism) (p : Point) : Point :=
  match f.toFun (.inl p) with | .inl q => q | .inr _ => 0

def autoFace (f : GraphAutomorphism) (j : Face) : Face :=
  match f.toFun (.inr j) with | .inr k => k | .inl _ => 0

theorem point_color_lt_four : ∀ p : Point, pointColor p < 4 := by decide +kernel

theorem auto_point_meaning (f : GraphAutomorphism) (p : Point) :
    f.toFun (.inl p) = .inl (autoPoint f p) := by
  have hc := automorphism_color f (.inl p)
  have hlt := point_color_lt_four p
  cases he : f.toFun (.inl p) with
  | inl q => simp [autoPoint, he]
  | inr j => simp only [he, graphColor] at hc; omega

theorem auto_face_meaning (f : GraphAutomorphism) (j : Face) :
    f.toFun (.inr j) = .inr (autoFace f j) := by
  have hc := automorphism_color f (.inr j)
  cases he : f.toFun (.inr j) with
  | inr k => simp [autoFace, he]
  | inl p =>
    have hlt := point_color_lt_four p
    simp only [he, graphColor] at hc
    omega

def reverseVertex : Vertex → Vertex
  | .inl p => .inl (reversePoint p)
  | .inr j => .inr (reverseFace j)

theorem all_automorphisms_exact (f : GraphAutomorphism) :
    f.toFun = id ∨ f.toFun = reverseVertex := by
  have ha : StablePoints (autoPoint f) := by
    intro p
    have hc := automorphism_color f (.inl p)
    simpa only [auto_point_meaning, graphColor] using hc
  have hb : StableFaces (autoFace f) := by
    intro j
    have hc := automorphism_color f (.inr j)
    simp only [auto_face_meaning, graphColor] at hc
    omega
  have he : IncidenceEndomorphism (autoPoint f) (autoFace f) := by
    intro p j h
    have hf := f.preserves (.inl p) (.inr j)
    simpa only [auto_point_meaning, auto_face_meaning, adjacent, h] using hf
  rcases stable_endomorphisms_exact _ _ ha hb he with hi | hr
  · left; funext v; cases v with
    | inl p => simpa [hi.1] using auto_point_meaning f p
    | inr j => simpa [hi.2] using auto_face_meaning f j
  · right; funext v; cases v with
    | inl p => simpa [hr.1, reverseVertex] using auto_point_meaning f p
    | inr j => simpa [hr.2, reverseVertex] using auto_face_meaning f j

def identityAutomorphism : GraphAutomorphism := ⟨id, id, fun _ => rfl, fun _ => rfl, fun _ _ => rfl⟩
def reversalAutomorphism : GraphAutomorphism where
  toFun := reverseVertex
  invFun := reverseVertex
  left_inv := by intro v; cases v <;> simp [reverseVertex, reversal_involutions]
  right_inv := by intro v; cases v <;> simp [reverseVertex, reversal_involutions]
  preserves := by intro u v; cases u <;> cases v <;> simp [reverseVertex, adjacent, reversal_incidence]

end T7
