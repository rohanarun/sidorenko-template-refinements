import T7Gap.StochasticCoefficient
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

theorem FiniteLaw.mean_const (law : FiniteLaw α) (r : Rat) : law.mean (fun _ => r) = r := by
  unfold FiniteLaw.mean
  have he : (fun s => law.weight s*r) = (fun s => r*law.weight s) := by funext s; grind only
  rw [he,rat_sum_mul,law.normalized]
  simp

theorem FiniteLaw.mean_add (law : FiniteLaw α) (f g : α → Rat) :
    law.mean (fun s => f s+g s) = law.mean f+law.mean g := by
  unfold FiniteLaw.mean
  have he : (fun s => law.weight s*(f s+g s)) =
      (fun s => law.weight s*f s+law.weight s*g s) := by funext s; grind only
  rw [he,rat_sum_add]

theorem FiniteLaw.mean_mul (law : FiniteLaw α) (r : Rat) (f : α → Rat) :
    law.mean (fun s => r*f s) = r*law.mean f := by
  unfold FiniteLaw.mean
  have he : (fun s => law.weight s*(r*f s)) = (fun s => r*(law.weight s*f s)) := by funext s; grind only
  rw [he,rat_sum_mul]

theorem FiniteLaw.mean_nonneg (law : FiniteLaw α) (f : α → Rat)
    (hf : ∀ s ∈ law.outcomes, 0 ≤ f s) : 0 ≤ law.mean f :=
  sum_rat_nonneg law.outcomes _ (fun s hs => Rat.mul_nonneg (law.nonnegative s hs) (hf s hs))

theorem FiniteLaw.mean_sum (law : FiniteLaw α) (xs : List β) (f : β → α → Rat) :
    law.mean (fun s => (xs.map fun i => f i s).sum) = (xs.map fun i => law.mean (f i)).sum := by
  induction xs with
  | nil => simp only [List.map_nil,List.sum_nil]; exact law.mean_const 0
  | cons x xs ih => simp only [List.map_cons,List.sum_cons]; rw [law.mean_add,ih]

theorem FiniteLaw.mean_comm (left : FiniteLaw α) (right : FiniteLaw β) (f : α → β → Rat) :
    left.mean (fun x => right.mean (f x)) = right.mean (fun y => left.mean (fun x => f x y)) := by
  change left.mean (fun x => (right.outcomes.map fun y => right.weight y*f x y).sum) = _
  rw [left.mean_sum]
  unfold FiniteLaw.mean at ⊢
  congr 1
  apply List.map_congr_left
  intro y _
  exact left.mean_mul _ _

theorem rat_sum_flatMap (xs : List α) (f : α → List Rat) :
    (xs.flatMap f).sum = (xs.map fun x => (f x).sum).sum := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [List.flatMap_cons,List.sum_append,List.map_cons,List.sum_cons,ih]

/-- n independent draws, enumerated with their actual product weights. -/
def productWeight (law : FiniteLaw α) : {n : Nat} → (Fin n → α) → Rat
  | 0, _ => 1
  | n+1, f => law.weight (f 0)*productWeight law (fun i : Fin n => f i.succ)

def independentMean (law : FiniteLaw α) (n : Nat) (f : (Fin n → α) → Rat) : Rat :=
  ((functions law.outcomes n).map fun s => productWeight law s*f s).sum

theorem independentMean_succ (law : FiniteLaw α) (f : (Fin (n+1) → α) → Rat) :
    independentMean law (n+1) f = law.mean (fun x => independentMean law n (fun s => f (Fin.cases x s))) := by
  unfold independentMean FiniteLaw.mean
  simp only [functions,List.map_flatMap,List.map_map,rat_sum_flatMap,Function.comp_def]
  congr 1
  apply List.map_congr_left
  intro x _
  rw [← rat_sum_mul]
  congr 1
  apply List.map_congr_left
  intro s _
  simp only [productWeight,Fin.cases_zero,Fin.cases_succ]
  grind only

theorem independentMean_const (law : FiniteLaw α) (n : Nat) (r : Rat) :
    independentMean law n (fun _ => r) = r := by
  induction n with
  | zero => simp [independentMean,functions,productWeight]; grind only
  | succ n ih => rw [independentMean_succ]; simp only [ih]; exact law.mean_const r

theorem productWeight_nonnegative (law : FiniteLaw α) (s : Fin n → α)
    (hs : ∀ i, s i ∈ law.outcomes) : 0 ≤ productWeight law s := by
  induction n with
  | zero => change (0:Rat) ≤ 1; decide +kernel
  | succ n ih => exact Rat.mul_nonneg (law.nonnegative _ (hs 0)) (ih _ (fun i => hs i.succ))

def independentLaw (law : FiniteLaw α) (n : Nat) : FiniteLaw (Fin n → α) where
  outcomes := functions law.outcomes n
  weight := productWeight law
  nonnegative := fun s hs => productWeight_nonnegative law s ((functions_mem _ _ _).mp hs)
  normalized := by
    have h := independentMean_const law n 1
    simpa only [independentMean,Rat.mul_one] using h

/-- Literal coordinate product, including the empty product. -/
def coordinateProduct : {n : Nat} → (Fin n → Rat) → Rat
  | 0, _ => 1
  | n+1, f => f 0*coordinateProduct (fun i : Fin n => f i.succ)

theorem coordinateProduct_one (n : Nat) : coordinateProduct (fun _ : Fin n => (1:Rat)) = 1 := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [coordinateProduct,Rat.one_mul,ih]

theorem coordinateProduct_nonneg (f : Fin n → Rat) (h : ∀ i, 0 ≤ f i) :
    0 ≤ coordinateProduct f := by
  induction n with
  | zero => change (0:Rat) ≤ 1; decide +kernel
  | succ n ih => exact Rat.mul_nonneg (h 0) (ih _ (fun i => h i.succ))

theorem independent_product (law : FiniteLaw α) (n : Nat) (f : Fin n → α → Rat) :
    (independentLaw law n).mean (fun s => coordinateProduct (fun i => f i (s i))) =
      coordinateProduct (fun i => law.mean (f i)) := by
  induction n with
  | zero => simp [FiniteLaw.mean,independentLaw,functions,productWeight,coordinateProduct]; decide +kernel
  | succ n ih =>
    change independentMean law (n+1) _ = _
    rw [independentMean_succ]
    simp only [coordinateProduct]
    have he : (fun x => independentMean law n (fun s => f 0 x * coordinateProduct (fun i => f i.succ (s i)))) =
        (fun x => f 0 x*coordinateProduct (fun i => law.mean (f i.succ))) := by
      funext x
      change (independentLaw law n).mean (fun s => f 0 x * coordinateProduct (fun i => f i.succ (s i))) = _
      rw [FiniteLaw.mean_mul,ih]
    change law.mean (fun x => independentMean law n (fun s => f 0 x*coordinateProduct (fun i => f i.succ (s i)))) = _
    rw [he]
    have hc : (fun x => f 0 x * coordinateProduct (fun i => law.mean (f i.succ))) =
        (fun x => coordinateProduct (fun i => law.mean (f i.succ))*f 0 x) := by funext x; grind only
    rw [hc,FiniteLaw.mean_mul]
    grind only

end T7Gap
