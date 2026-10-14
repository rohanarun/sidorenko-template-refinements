import T7Weighted
import Lean
open Lean Elab Command
set_option pp.universes true
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let fromProject := fun name => match env.getModuleIdxFor? name with
    | some idx =>
      let modName := env.header.moduleNames[idx.toNat]!
      (`T7).isPrefixOf modName || (`T7Gap).isPrefixOf modName || (`T7Weighted).isPrefixOf modName
    | none => false
  let names := env.constants.toList.map Prod.fst |>.filter fromProject |>.toArray.qsort Name.lt
  for name in names do
    let some info := env.find? name | throwError "missing declaration {name}"
    let axs ← collectAxioms name
    let kind := match info with
      | .thmInfo _ => "theorem"
      | .axiomInfo _ => "axiom"
      | .defnInfo _ => "definition"
      | .opaqueInfo _ => "opaque"
      | .inductInfo _ => "inductive"
      | .ctorInfo _ => "constructor"
      | .recInfo _ => "recursor"
      | .quotInfo _ => "quotient"
    let deps := info.type.getUsedConstants.toList
    let bodyDeps := match info.value? true with
      | some value => value.getUsedConstants.toList
      | none => []
    logInfo s!"DECL|{name}|{kind}|{String.intercalate "," (axs.toList.map toString)}|{String.intercalate "," (deps.eraseDups.map toString)}|{String.intercalate "," (bodyDeps.eraseDups.map toString)}"
