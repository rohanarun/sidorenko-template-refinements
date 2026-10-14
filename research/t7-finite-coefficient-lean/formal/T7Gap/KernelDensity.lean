import T7Gap.TypedKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

theorem independentLaw_succ_mean (law : FiniteLaw α) (f : (Fin (n+1) → α) → Rat) :
    (independentLaw law (n+1)).mean f =
    law.mean (fun x => (independentLaw law n).mean (fun s => f (Fin.cases x s))) :=
  independentMean_succ law f

theorem fst_cons (p : X × Y) (s : Fin n → X × Y) :
    (fun i : Fin (n+1) => ((Fin.cases p s i) : X × Y).1) = Fin.cases p.1 (fun i => (s i).1) := by
  funext i
  cases i using Fin.cases <;> rfl

theorem snd_cons (p : X × Y) (s : Fin n → X × Y) :
    (fun i : Fin (n+1) => ((Fin.cases p s i) : X × Y).2) = Fin.cases p.2 (fun i => (s i).2) := by
  funext i
  cases i using Fin.cases <;> rfl

/-- Actual independence of the two vector projections under an n-fold product law. -/
theorem independent_productLaw (left : FiniteLaw X) (right : FiniteLaw Y) (n : Nat)
    (f : (Fin n → X) → (Fin n → Y) → Rat) :
    (independentLaw (productLaw left right) n).mean (fun s => f (fun i => (s i).1) (fun i => (s i).2)) =
    (independentLaw left n).mean (fun x => (independentLaw right n).mean (f x)) := by
  induction n with
  | zero =>
    simp [FiniteLaw.mean,independentLaw,functions,productWeight]
    have hx : (fun i : Fin 0 => (Fin.elim0 i : X × Y).1) = (fun i => Fin.elim0 i) := by funext i; exact Fin.elim0 i
    have hy : (fun i : Fin 0 => (Fin.elim0 i : X × Y).2) = (fun i => Fin.elim0 i) := by funext i; exact Fin.elim0 i
    rw [hx,hy]
    grind only
  | succ n ih =>
    rw [independentLaw_succ_mean,productLaw_mean]
    simp only [fst_cons,snd_cons]
    have he (x : X) (y : Y) := ih (fun xs ys => f (Fin.cases x xs) (Fin.cases y ys))
    simp only [he]
    rw [independentLaw_succ_mean]
    congr 1
    funext x
    rw [FiniteLaw.mean_comm]
    congr 1
    funext xs
    rw [independentLaw_succ_mean]

theorem coordinateProduct_mul (f g : Fin n → Rat) :
    coordinateProduct (fun i => f i*g i) = coordinateProduct f*coordinateProduct g := by
  induction n with
  | zero => simp [coordinateProduct]
  | succ n ih =>
    simp only [coordinateProduct]
    rw [ih]
    grind only

theorem separated_four_means (A : FiniteLaw α) (B : FiniteLaw β) (C : FiniteLaw γ) (D : FiniteLaw δ)
    (f : α → δ → Rat) (g : β → γ → Rat) :
    A.mean (fun a => B.mean (fun b => C.mean (fun c => D.mean (fun d => f a d*g b c)))) =
      (A.mean (fun a => D.mean (f a)))*(B.mean (fun b => C.mean (g b))) := by
  have hd (a : α) (b : β) (c : γ) : D.mean (fun d => f a d*g b c) = g b c*D.mean (f a) := by
    have he : (fun d => f a d*g b c) = (fun d => g b c*f a d) := by funext d; grind only
    rw [he,FiniteLaw.mean_mul]
  simp only [hd]
  have hc (a : α) (b : β) : C.mean (fun c => g b c*D.mean (f a)) = D.mean (f a)*C.mean (g b) := by
    have he : (fun c => g b c*D.mean (f a)) = (fun c => D.mean (f a)*g b c) := by funext c; grind only
    rw [he,FiniteLaw.mean_mul]
  simp only [hc,FiniteLaw.mean_mul]
  have he : (fun a => D.mean (f a)*(B.mean fun b => C.mean (g b))) =
      (fun a => (B.mean fun b => C.mean (g b))*D.mean (f a)) := by funext a; grind only
  rw [he,FiniteLaw.mean_mul]
  grind only

def transposeKernel (W : RationalBipartiteKernel X Y) : RationalBipartiteKernel Y X where
  left := W.right
  right := W.left
  value := fun y x => W.value x y
  nonnegative := fun y x => W.nonnegative x y

/-- Source section 8's density factorization, for the actual constructed symmetric kernel. -/
theorem symmetricProduct_density (W : RationalBipartiteKernel X Y) :
    (symmetricProductKernel W).density = W.density*(transposeKernel W).density := by
  change (independentLaw (productLaw W.left W.right) 7).mean (fun x =>
    (independentLaw (productLaw W.left W.right) 10).mean (fun y =>
      coordinateProduct (fun c : Corner => W.value (x (corner c).1).1 (y (corner c).2).2 *
        W.value (y (corner c).2).1 (x (corner c).1).2))) = _
  have hinner (x : Point → X × Y) := independent_productLaw W.left W.right 10
    (fun xj yj => coordinateProduct (fun c : Corner => W.value (x (corner c).1).1 (yj (corner c).2) *
      W.value (xj (corner c).2) (x (corner c).1).2))
  simp only [hinner]
  have houter := independent_productLaw W.left W.right 7
    (fun xi yi => (independentLaw W.left 10).mean (fun xj => (independentLaw W.right 10).mean
      (fun yj => coordinateProduct (fun c : Corner => W.value (xi (corner c).1) (yj (corner c).2) *
        W.value (xj (corner c).2) (yi (corner c).1)))))
  rw [houter]
  simp only [coordinateProduct_mul]
  rw [separated_four_means]
  rfl

end T7Gap
