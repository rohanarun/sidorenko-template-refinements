import T7Gap.KernelDensity
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

/-- An actual rational Bernoulli law, with true having probability p. -/
def bernoulliLaw (p : Rat) (hp : 0 ≤ p) (h1 : p ≤ 1) : FiniteLaw Bool where
  outcomes := [true,false]
  weight := fun b => if b then p else 1-p
  nonnegative := by
    intro b _
    cases b
    · change 0 ≤ 1-p
      grind only
    · exact hp
  normalized := by simp; grind only

theorem bernoulli_mean (p : Rat) (hp : 0 ≤ p) (h1 : p ≤ 1) (f : Bool → Rat) :
    (bernoulliLaw p hp h1).mean f = p*f true+(1-p)*f false := by
  simp [FiniteLaw.mean,bernoulliLaw]
  grind only

def pairObservable (base : SignedBase X Y) (p : Point) (j : Face)
    (x : Fin 30 → X) (y : Fin 30 → Y) (o : ActivationOutcome) : Rat :=
  if incident p j then coordinateProduct (fun i : Corner =>
    if activationSupport (cornerIndex p j) o.1 i then base.value (o.2 i) (x i) (y i) else 1) else 1

theorem pairKernel_eq_expectation (base : SignedBase X Y) (p : Point) (j : Face)
    (x : Fin 30 → X) (y : Fin 30 → Y) :
    pairKernel base p j x y = (activationLaw (cornerIndex p j)).mean (pairObservable base p j x y) := by
  unfold pairKernel pairObservable
  by_cases h : incident p j = true
  · simp only [h,ite_true]
    rfl
  · simp [h,FiniteLaw.mean_const]

/-- The activation/empty-law choice is one Bernoulli draw for the entire corner. -/
def thinnedActivationLaw (p : Point) (j : Face) : FiniteLaw (Bool × ActivationOutcome) :=
  productLaw (bernoulliLaw (thinning p j) (by have h := (thinning_bounds p j).1; grind only)
    (thinning_bounds p j).2) (activationLaw (cornerIndex p j))

def thinnedObservable (base : SignedBase X Y) (p : Point) (j : Face)
    (x : Fin 30 → X) (y : Fin 30 → Y) (o : Bool × ActivationOutcome) : Rat :=
  if o.1 then pairObservable base p j x y o.2 else 1

/-- Formula (6)'s expectation, including exactly one thinning trial per source incidence. -/
theorem thinnedPairKernel_eq_expectation (base : SignedBase X Y) (p : Point) (j : Face)
    (x : Fin 30 → X) (y : Fin 30 → Y) :
    thinnedPairKernel base p j x y = (thinnedActivationLaw p j).mean (thinnedObservable base p j x y) := by
  unfold thinnedActivationLaw
  rw [productLaw_mean,bernoulli_mean]
  simp only [thinnedObservable,Bool.false_eq_true,ite_true,ite_false,FiniteLaw.mean_const,Rat.mul_one]
  unfold thinnedPairKernel
  rw [pairKernel_eq_expectation]

end T7Gap
