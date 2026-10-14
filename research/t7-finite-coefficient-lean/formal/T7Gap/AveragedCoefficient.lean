import T7Gap.KernelScale
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

def thinnedFeature (p : Point) (j : Face) (a : Mask) (o : Bool × ActivationOutcome) : Rat :=
  if o.1 then pairFeature p j a o.2 else if IsZero a then 1 else 0

def thinnedMoment (p : Point) (j : Face) (a b : Mask) : Rat :=
  (thinnedActivationLaw p j).mean (fun o => thinnedFeature p j a o*thinnedFeature p j b o)

theorem thinnedMoment_factor (p : Point) (j : Face) (a b : Mask) (ha : NonemptyMask a) :
    thinnedMoment p j a b = thinning p j*pairMoment p j a b := by
  have hne : ¬ IsZero a := by
    obtain ⟨c,hc⟩ := ha
    intro hz
    have ht := hz c
    rw [hc] at ht
    contradiction
  unfold thinnedMoment thinnedActivationLaw
  rw [productLaw_mean,bernoulli_mean]
  simp [thinnedFeature,hne,pairMoment,FiniteLaw.mean_const]
  grind only

def thinnedCoefficient (a : Point → Point) (b : Face → Face) : Rat :=
  (allLabelings.map fun labels => ((List.finRange 30).map fun c =>
    thinnedMoment (a (corner c).1) (b (corner c).2)
      (labels (leftEdge c)) (labels (rightEdge c))).prod).sum

theorem rat_prod_mul (xs : List α) (f g : α → Rat) :
    (xs.map fun x => f x*g x).prod = (xs.map f).prod*(xs.map g).prod := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp only [List.map_cons,List.prod_cons,ih]; grind only

/-- One thinning factor per source incidence, independent of the number of active coordinates. -/
theorem thinnedCoefficient_factor (a : Point → Point) (b : Face → Face) :
    thinnedCoefficient a b =
    ((List.finRange 30).map fun c => thinning (a (corner c).1) (b (corner c).2)).prod*generalCoefficient a b := by
  unfold thinnedCoefficient generalCoefficient
  rw [← rat_sum_mul]
  congr 1
  apply List.map_congr_left
  intro labels hl
  have hn := (labelings_mem labels).mp hl
  simp only [thinnedMoment_factor _ _ _ _ (hn _)]
  exact rat_prod_mul _ _ _

/-- The actual finite expectation over independent source type draws, before any score estimate. -/
def averagedCoefficient : Rat :=
  (independentLaw pointPrior 7).mean (fun a => (independentLaw facePrior 10).mean (thinnedCoefficient a))

/-- The averaging and thinning formula is connected to the actual distributions. Negativity is not assumed. -/
theorem averagedCoefficient_exact : averagedCoefficient =
    ((functions pointPrior.outcomes 7).map fun a =>
      productWeight pointPrior a * ((functions facePrior.outcomes 10).map fun b =>
        productWeight facePrior b * (((List.finRange 30).map fun c =>
          thinning (a (corner c).1) (b (corner c).2)).prod*generalCoefficient a b)).sum).sum := by
  unfold averagedCoefficient
  simp only [FiniteLaw.mean,independentLaw,thinnedCoefficient_factor]

end T7Gap
