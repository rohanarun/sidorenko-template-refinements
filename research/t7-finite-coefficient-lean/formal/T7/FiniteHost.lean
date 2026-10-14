import T7.Transfer
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7

/-- Finite simple hosts have an explicit loop-free symmetric adjacency table. -/
structure SimpleHost (n : Nat) where
  adj : Fin n → Fin n → Bool
  symmetric : ∀ u v, adj u v = adj v u
  loop_free : ∀ u, adj u u = false

def SimpleHost.edgeDensity {n : Nat} (G : SimpleHost n) : Rat :=
  (((List.finRange n).flatMap fun u => (List.finRange n).filter (G.adj u)).length : Rat) / (n:Rat)^2

def SimpleHost.homDensity {n : Nat} (G : SimpleHost n) : Rat :=
  let assignments := (functions (List.finRange n) 7).flatMap fun a =>
    (functions (List.finRange n) 10).map fun b => (a,b)
  let good := assignments.filter fun (a,b) =>
    (List.finRange 30).all fun c => G.adj (a (corner c).1) (b (corner c).2)
  (good.length : Rat) / (n:Rat)^17

def expectation (outcomes : List α) (weight : α → Rat) (f : α → Rat) : Rat :=
  (outcomes.map fun x => weight x * f x).sum

theorem sum_rat_le (l : List α) (f g : α → Rat)
    (h : ∀ x ∈ l, f x ≤ g x) : (l.map f).sum ≤ (l.map g).sum := by
  induction l with
  | nil => simp
  | cons x xs ih =>
    have h0 := h x (by simp)
    have h1 := ih (fun y hy => h y (by simp [hy]))
    simp only [List.map_cons, List.sum_cons]
    grind

theorem expectation_witness (outcomes : List α) (weight f g : α → Rat)
    (hw : ∀ x ∈ outcomes, 0 ≤ weight x)
    (hgap : expectation outcomes weight f < expectation outcomes weight g) :
    ∃ x ∈ outcomes, f x < g x := by
  classical
  by_cases hh : ∃ x ∈ outcomes, f x < g x
  · exact hh
  · have hle : ∀ x ∈ outcomes, g x ≤ f x := by
      intro x hx
      have hn : ¬ f x < g x := fun h => hh ⟨x,hx,h⟩
      grind
    have hs := sum_rat_le outcomes (fun x => weight x * g x) (fun x => weight x * f x)
      (fun x hx => Rat.mul_le_mul_of_nonneg_left (hle x hx) (hw x hx))
    unfold expectation at hgap
    grind

/-- Numerical finite-host argument. Collision, Jensen and Bernoulli bounds are explicit hypotheses.
This theorem does not assert that a sampling process satisfying those hypotheses has been built. -/
theorem finite_host_from_sampling_bounds {n : Nat}
    (outcomes : List (SimpleHost n)) (weight : SimpleHost n → Rat)
    (mu kernelDensity delta invN : Rat)
    (hw : ∀ G ∈ outcomes, 0 ≤ weight G)
    (hdelta : delta = mu^30-kernelDensity)
    (hsize : (136+30*mu^30)*invN < delta)
    (hcollision : expectation outcomes weight SimpleHost.homDensity ≤ kernelDensity+136*invN)
    (hmean : expectation outcomes weight SimpleHost.edgeDensity = (1-invN)*mu)
    (hbernoulli : (1-30*invN)*mu^30 ≤ ((1-invN)*mu)^30)
    (hjensen : (expectation outcomes weight SimpleHost.edgeDensity)^30 ≤
      expectation outcomes weight (fun G => G.edgeDensity^30)) :
    ∃ G ∈ outcomes, G.homDensity < G.edgeDensity^30 := by
  apply expectation_witness outcomes weight SimpleHost.homDensity (fun G => G.edgeDensity^30) hw
  rw [hmean] at hjensen
  grind

/-- Conversion of the packet's N threshold into the hypothesis used above. -/
theorem sufficient_host_size (mu delta N : Rat)
    (hdelta : 0 < delta) (hN : 0 < N)
    (hsize : (136+30*mu^30)/delta < N) :
    (136+30*mu^30)*(1/N) < delta := by
  have hh := (Rat.div_lt_iff hdelta).mp hsize
  have he : (136+30*mu^30)*(1/N) = (136+30*mu^30)/N := by grind
  rw [he]
  apply (Rat.div_lt_iff hN).mpr
  grind

end T7
