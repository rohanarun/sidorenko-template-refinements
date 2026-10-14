import Std
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7
abbrev Point := Fin 7
abbrev Face := Fin 10
abbrev Corner := Fin 30
abbrev Edge := Fin 15
abbrev Vertex := Sum Point Face
def face : Fin 10 → List Point
  | ⟨0, _⟩ => [0, 1, 2]
  | ⟨1, _⟩ => [0, 1, 3]
  | ⟨2, _⟩ => [0, 2, 3]
  | ⟨3, _⟩ => [1, 2, 4]
  | ⟨4, _⟩ => [1, 3, 4]
  | ⟨5, _⟩ => [2, 3, 5]
  | ⟨6, _⟩ => [2, 4, 5]
  | ⟨7, _⟩ => [3, 4, 6]
  | ⟨8, _⟩ => [3, 5, 6]
  | ⟨9, _⟩ => [4, 5, 6]
def pointEdge : Fin 15 → Point × Point
  | ⟨0, _⟩ => (0, 1)
  | ⟨1, _⟩ => (0, 2)
  | ⟨2, _⟩ => (0, 3)
  | ⟨3, _⟩ => (1, 2)
  | ⟨4, _⟩ => (1, 3)
  | ⟨5, _⟩ => (1, 4)
  | ⟨6, _⟩ => (2, 3)
  | ⟨7, _⟩ => (2, 4)
  | ⟨8, _⟩ => (2, 5)
  | ⟨9, _⟩ => (3, 4)
  | ⟨10, _⟩ => (3, 5)
  | ⟨11, _⟩ => (3, 6)
  | ⟨12, _⟩ => (4, 5)
  | ⟨13, _⟩ => (4, 6)
  | ⟨14, _⟩ => (5, 6)
def corner : Fin 30 → Point × Face
  | ⟨0, _⟩ => (0, 0)
  | ⟨1, _⟩ => (1, 0)
  | ⟨2, _⟩ => (2, 0)
  | ⟨3, _⟩ => (0, 1)
  | ⟨4, _⟩ => (1, 1)
  | ⟨5, _⟩ => (3, 1)
  | ⟨6, _⟩ => (0, 2)
  | ⟨7, _⟩ => (2, 2)
  | ⟨8, _⟩ => (3, 2)
  | ⟨9, _⟩ => (1, 3)
  | ⟨10, _⟩ => (2, 3)
  | ⟨11, _⟩ => (4, 3)
  | ⟨12, _⟩ => (1, 4)
  | ⟨13, _⟩ => (3, 4)
  | ⟨14, _⟩ => (4, 4)
  | ⟨15, _⟩ => (2, 5)
  | ⟨16, _⟩ => (3, 5)
  | ⟨17, _⟩ => (5, 5)
  | ⟨18, _⟩ => (2, 6)
  | ⟨19, _⟩ => (4, 6)
  | ⟨20, _⟩ => (5, 6)
  | ⟨21, _⟩ => (3, 7)
  | ⟨22, _⟩ => (4, 7)
  | ⟨23, _⟩ => (6, 7)
  | ⟨24, _⟩ => (3, 8)
  | ⟨25, _⟩ => (5, 8)
  | ⟨26, _⟩ => (6, 8)
  | ⟨27, _⟩ => (4, 9)
  | ⟨28, _⟩ => (5, 9)
  | ⟨29, _⟩ => (6, 9)
  | ⟨n+30, h⟩ => by omega

def incident (p : Point) (j : Face) : Bool := (face j).contains p
def adjacent : Vertex → Vertex → Bool
  | .inl p, .inr j => incident p j
  | .inr j, .inl p => incident p j
  | _, _ => false
def vertices : List Vertex := (List.finRange 7).map Sum.inl ++ (List.finRange 10).map Sum.inr
def incidenceEdges : List (Point × Face) := (List.finRange 7).flatMap fun p =>
  ((List.finRange 10).filter (incident p)).map fun j => (p,j)
def degree (p : Point) : Nat := ((List.finRange 10).filter (incident p)).length
def pointColor (p : Point) : Nat := min p.val (6-p.val)
def faceColor (j : Face) : Nat := min j.val (9-j.val)
def reversePoint (p : Point) : Point := ⟨6-p.val, by omega⟩
def reverseFace (j : Face) : Face := ⟨9-j.val, by omega⟩

theorem vertex_count : vertices.length = 17 := by decide +kernel
theorem incidence_edge_count : incidenceEdges.length = 30 := by decide +kernel
theorem vertices_nodup : vertices.Nodup := by decide +kernel
theorem incidence_edges_nodup : incidenceEdges.Nodup := by decide +kernel
theorem all_corners : List.ofFn corner = (List.finRange 10).flatMap
    (fun j => (face j).map fun p => (p,j)) := by decide +kernel
theorem corner_bijection : (∀ c d, corner c = corner d → c = d) ∧
    (∀ p j, incident p j = true ↔ ∃ c, corner c = (p,j)) := by decide +kernel
theorem adjacency_symmetric : ∀ u v, adjacent u v = adjacent v u := by
  intro u v; cases u <;> cases v <;> rfl
theorem adjacency_irreflexive : ∀ u, adjacent u u = false := by
  intro u; cases u <;> rfl
theorem degrees : List.ofFn degree = [3,4,5,6,5,4,3] := by decide +kernel
theorem point_cells_by_degree : ∀ p q, pointColor p = pointColor q ↔ degree p = degree q := by decide +kernel

def pointSignature (p : Point) : List Nat := (List.range 5).map fun c =>
  ((List.finRange 10).filter fun j => incident p j && (faceColor j == c)).length
def faceSignature (j : Face) : List Nat := (List.range 4).map fun c =>
  ((face j).filter fun p => pointColor p == c).length

theorem stable_partition :
    (∀ p q, pointColor p = pointColor q → pointSignature p = pointSignature q) ∧
    (∀ j k, faceColor j = faceColor k → faceSignature j = faceSignature k) := by decide +kernel
theorem face_cells_by_point_signature : ∀ j k,
    faceColor j = faceColor k ↔ faceSignature j = faceSignature k := by decide +kernel
theorem reversal_incidence : ∀ p j,
    incident (reversePoint p) (reverseFace j) = incident p j := by decide +kernel
theorem reversal_involutions :
    (∀ p, reversePoint (reversePoint p) = p) ∧
    (∀ j, reverseFace (reverseFace j) = j) := by decide +kernel

end T7
