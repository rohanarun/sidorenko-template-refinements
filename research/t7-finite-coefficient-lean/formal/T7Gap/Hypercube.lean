import T7.HostConclusion
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

abbrev Bits (n : Nat) := Fin n → Bool

def bitSign (b : Bool) : Rat := if b then -1 else 1
def bitFactor (a b : Bool) : Rat := if a then bitSign b else 1

def char : {n : Nat} → Bits n → Bits n → Rat
  | 0, _, _ => 1
  | n+1, a, s => bitFactor (a 0) (s 0) *
      char (fun i : Fin n => a i.succ) (fun i => s i.succ)

def zeroBits (n : Nat) : Bits n := fun _ => false
def xorBits (a b : Bits n) : Bits n := fun i => xor (a i) (b i)
def IsZero (a : Bits n) : Prop := ∀ i, a i = false
instance (a : Bits n) : Decidable (IsZero a) := inferInstanceAs (Decidable (∀ i, a i = false))

def cubeSum (n : Nat) (f : Bits n → Rat) : Rat := ((functions [false,true] n).map f).sum
def cubeAvg (n : Nat) (f : Bits n → Rat) : Rat := cubeSum n f / 2^n

theorem rat_sum_add (xs : List α) (f g : α → Rat) :
    (xs.map fun x => f x+g x).sum = (xs.map f).sum+(xs.map g).sum := by
  induction xs with
  | nil => simp; decide +kernel
  | cons x xs ih => simp only [List.map_cons, List.sum_cons]; rw [ih]; grind

theorem rat_sum_mul (xs : List α) (r : Rat) (f : α → Rat) :
    (xs.map fun x => r*f x).sum = r*(xs.map f).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp only [List.map_cons, List.sum_cons]; rw [ih]; grind

theorem cubeSum_add (f g : Bits n → Rat) :
    cubeSum n (fun s => f s+g s) = cubeSum n f+cubeSum n g := rat_sum_add _ _ _

theorem cubeSum_mul (r : Rat) (f : Bits n → Rat) :
    cubeSum n (fun s => r*f s) = r*cubeSum n f := rat_sum_mul _ _ _

theorem cubeSum_succ (f : Bits (n+1) → Rat) : cubeSum (n+1) f =
    cubeSum n (fun s => f (Fin.cases false s)) + cubeSum n (fun s => f (Fin.cases true s)) := by
  simp [cubeSum, functions, List.map_append, List.sum_append, List.map_map, Function.comp_def]

theorem cubeSum_const (n : Nat) (r : Rat) : cubeSum n (fun _ => r) = 2^n*r := by
  induction n with
  | zero => simp [cubeSum, functions]; grind
  | succ n ih => rw [cubeSum_succ]; simp only [ih, Rat.pow_succ]; grind

theorem char_mul (a b s : Bits n) : char a s*char b s = char (xorBits a b) s := by
  induction n with
  | zero => simp [char]
  | succ n ih =>
    have hi := ih (fun i => a i.succ) (fun i => b i.succ) (fun i => s i.succ)
    have hb : ∀ x y z : Bool,
        bitFactor x z*bitFactor y z = bitFactor (xor x y) z := by decide +kernel
    have hbit := hb (a 0) (b 0) (s 0)
    simp only [char]
    change (bitFactor (a 0) (s 0)*char (fun i => a i.succ) (fun i => s i.succ))*
      (bitFactor (b 0) (s 0)*char (fun i => b i.succ) (fun i => s i.succ)) =
      bitFactor (xor (a 0) (b 0)) (s 0)*char (fun i => xor (a i.succ) (b i.succ)) (fun i => s i.succ)
    change char (fun i => a i.succ) (fun i => s i.succ) *
      char (fun i => b i.succ) (fun i => s i.succ) =
      char (fun i => xor (a i.succ) (b i.succ)) (fun i => s i.succ) at hi
    rw [← hi, ← hbit]
    clear ih hb
    grind only

theorem char_zero (s : Bits n) : char (zeroBits n) s = 1 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [char, zeroBits,bitFactor] at *; exact ih (fun i => s i.succ)

theorem char_sign (a s : Bits n) : char a s = 1 ∨ char a s = -1 := by
  induction n with
  | zero => exact Or.inl rfl
  | succ n ih =>
    have h := ih (fun i => a i.succ) (fun i => s i.succ)
    simp only [char]
    cases a 0 <;> cases s 0 <;> simp only [bitFactor,bitSign,ite_false,ite_true] <;> grind

theorem IsZero_succ (a : Bits (n+1)) : IsZero a ↔ a 0 = false ∧ IsZero (fun i : Fin n => a i.succ) :=
  Fin.forall_fin_succ

theorem cubeSum_char (n : Nat) (a : Bits n) :
    cubeSum n (char a) = if IsZero a then 2^n else 0 := by
  induction n with
  | zero =>
    have hz : IsZero a := fun i => Fin.elim0 i
    simp [cubeSum,functions,char,hz]; decide +kernel
  | succ n ih =>
    rw [cubeSum_succ]
    have hf : (fun s => char a (Fin.cases false s)) =
        (fun s => (if a 0 then (1:Rat) else 1)*char (fun i : Fin n => a i.succ) s) := rfl
    have ht : (fun s => char a (Fin.cases true s)) =
        (fun s => (if a 0 then (-1:Rat) else 1)*char (fun i : Fin n => a i.succ) s) := rfl
    rw [hf,ht,cubeSum_mul,cubeSum_mul,ih]
    simp only [IsZero_succ]
    cases h : a 0 <;> by_cases hz : IsZero (fun i : Fin n => a i.succ) <;>
      simp [h,hz,Rat.pow_succ] <;> grind

theorem cubeAvg_char (a : Bits n) : cubeAvg n (char a) = if IsZero a then 1 else 0 := by
  unfold cubeAvg
  rw [cubeSum_char]
  have hp : (2:Rat)^n ≠ 0 := by have h := Rat.pow_pos (n := n) (by decide +kernel : (0:Rat)<2); grind
  by_cases hz : IsZero a <;> simp only [hz,ite_true,ite_false,Rat.div_def]
  · exact Rat.mul_inv_cancel _ hp
  · simp

end T7Gap
