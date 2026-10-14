import T7.Coefficient
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7

/-- Exhaustive finite function enumeration. This definition is symbolic for the large label space. -/
def functions (values : List α) : (n : Nat) → List (Fin n → α)
  | 0 => [fun i => Fin.elim0 i]
  | n+1 => values.flatMap fun x => (functions values n).map fun f => Fin.cases x f

theorem functions_mem (values : List α) (n : Nat) (f : Fin n → α) :
    f ∈ functions values n ↔ ∀ i, f i ∈ values := by
  induction n with
  | zero =>
    have hf : f = fun i => Fin.elim0 i := by funext i; exact Fin.elim0 i
    simp [functions, hf]
  | succ n ih =>
    constructor
    · intro h i
      obtain ⟨x, hx, hmap⟩ := List.mem_flatMap.mp h
      obtain ⟨g, hg, rfl⟩ := List.mem_map.mp hmap
      exact Fin.cases hx (fun j => (ih g).mp hg j) i
    · intro h
      apply List.mem_flatMap.mpr
      refine ⟨f 0, h 0, List.mem_map.mpr ?_⟩
      refine ⟨fun i => f i.succ, (ih _).mpr (fun i => h i.succ), ?_⟩
      funext i
      exact Fin.cases rfl (fun _ => rfl) i

theorem functions_nodup (values : List α) (hv : values.Nodup) (n : Nat) :
    (functions values n).Nodup := by
  induction n with
  | zero => simp [functions]
  | succ n ih =>
    apply List.pairwise_flatMap.mpr
    constructor
    · intro x hx
      apply List.pairwise_map.mpr
      apply List.Pairwise.imp (l := functions values n) _ ih
      intro f g hfg he
      apply hfg
      funext i
      exact congrFun he i.succ
    · apply List.Pairwise.imp (l := values) _ hv
      intro x y hxy f hf g hg he
      obtain ⟨f', hf', rfl⟩ := List.mem_map.mp hf
      obtain ⟨g', hg', rfl⟩ := List.mem_map.mp hg
      exact hxy (congrFun he 0)

def allMasks : List Mask := functions [false,true] 30
def nonemptyMasks : List Mask := allMasks.filter fun a => decide (NonemptyMask a)
def allLabelings : List Labeling := functions nonemptyMasks 15

theorem all_masks_complete (a : Mask) : a ∈ allMasks := by
  apply (functions_mem _ _ _).mpr
  intro i
  cases a i <;> simp

theorem nonempty_masks_mem (a : Mask) : a ∈ nonemptyMasks ↔ NonemptyMask a := by
  simp only [nonemptyMasks, List.mem_filter, decide_eq_true_eq]
  exact ⟨fun h => h.2, fun h => ⟨all_masks_complete a, h⟩⟩

theorem labelings_mem (a : Labeling) : a ∈ allLabelings ↔ ∀ e, NonemptyMask (a e) := by
  rw [allLabelings, functions_mem]
  exact forall_congr' (fun _ => nonempty_masks_mem _)

theorem labelings_nodup : allLabelings.Nodup := by
  apply functions_nodup
  apply List.Pairwise.filter
  apply functions_nodup
  decide

theorem support_nonempty : ∀ e, NonemptyMask (support e) := by decide +kernel

theorem sum_zero (l : List α) (f : α → Int) (h : ∀ a ∈ l, f a = 0) : (l.map f).sum = 0 := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
    simp only [List.map_cons, List.sum_cons]
    rw [h x (by simp), ih (fun a ha => h a (by simp [ha]))]
    rfl

theorem sum_single (l : List α) (f : α → Int) (s : α)
    (hn : l.Nodup) (hs : s ∈ l)
    (hz : ∀ a ∈ l, a ≠ s → f a = 0) : (l.map f).sum = f s := by
  induction l with
  | nil => simp at hs
  | cons x xs ih =>
    have hn' := List.nodup_cons.mp hn
    simp only [List.mem_cons] at hs
    simp only [List.map_cons, List.sum_cons]
    rcases hs with he | ht
    · subst x
      have hzero : (xs.map f).sum = 0 := sum_zero xs f (by
        intro a ha
        apply hz a (by simp [ha])
        intro h; subst a; exact hn'.1 ha)
      rw [hzero]; exact Int.add_zero _
    · have hxs : x ≠ s := by intro h; subst x; exact hn'.1 ht
      rw [hz x (by simp) hxs, ih hn'.2 ht (fun a ha => hz a (by simp [ha]))]
      exact Int.zero_add _

/-- The actual all-nonempty coefficient index set: (2^30-1)^15 assignments. -/
def fullCoefficient : Rat := ((allLabelings.map termNumerator).sum : Rat) / 4^30

theorem full_numerator : (allLabelings.map termNumerator).sum = -1 := by
  rw [sum_single allLabelings termNumerator support labelings_nodup
    ((labelings_mem support).mpr support_nonempty)]
  · exact canonical_numerator
  · intro a ha hn
    exact noncanonical_term_zero a ((labelings_mem a).mp ha) hn

theorem full_coefficient_exact : fullCoefficient = -(1 / 4^30 : Rat) := by
  unfold fullCoefficient
  rw [full_numerator]
  decide +kernel

end T7
