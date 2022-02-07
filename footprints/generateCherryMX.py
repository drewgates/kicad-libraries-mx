import os
import itertools

sizesToGenerate=["1.00", "1.25", "1.50", "1.75", "2.00", "2.25", "2.50", "2.75", "3.00", "4.00", "4.50", "5.50", "6.00", "6.25", "6.50", "7.00", "8.00", "9.00", "9.75", "10.00"]

# All of the dimensions are in mm
unit = 19.05

# Spacings taken from https://cdn.sparkfun.com/datasheets/Components/Switches/MX%20Series.pdf and https://deskthority.net/wiki/Space_bar_dimensions
stabSpacings = {
  "2.00": 0.94*25.4,
  "2.25": 0.94*25.4,
  "2.50": 0.94*25.4,
  "2.75": 0.94*25.4,
  "3.00": 1.5*25.4,
  "4.00": 2.25*25.4,
  "4.50": 2.73*25.4,
  "5.50": 3.375*25.4,
  "6.00": 3*25.4,
  "6.25": 100,
  "6.50": 4.125*25.4,
  "7.00": 4.5*25.4,
  "8.00": 5.25*25.4,
  "9.00": 5.25*25.4,
  "9.75": 5.25*25.4,
  "10.00": 5.25*25.4,
}

componentsList = {
  "BaseStart": """
(module {name} (layer F.Cu) (tedit 5E866FEB)
  (descr "{description}")
  (tags "{keywords}")
  (fp_text reference REF** (at 0 -8.6625) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value {name} (at 0 8.6625) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_line (start 7 7) (end -7 7) (layer F.SilkS) (width 0.12))
  (fp_line (start 7 -7) (end 7 7) (layer F.SilkS) (width 0.12))
  (fp_line (start -7 -7) (end 7 -7) (layer F.SilkS) (width 0.12))
  (fp_line (start -7 -7) (end -7 7) (layer F.SilkS) (width 0.12))
  (fp_line (start -7.8 -7.8) (end 7.8 -7.8) (layer F.Fab) (width 0.12))
  (fp_line (start -7.8 -7.8) (end -7.8 7.8) (layer F.Fab) (width 0.12))
  (fp_line (start 7.8 -7.8) (end 7.8 7.8) (layer F.Fab) (width 0.12))
  (fp_line (start -7.8 7.8) (end 7.8 7.8) (layer F.Fab) (width 0.12))
  (fp_line (start -{outlineSize} 9.525) (end -{outlineSize} -9.525) (layer Dwgs.User) (width 0.12))
  (fp_line (start {outlineSize} 9.525) (end -{outlineSize} 9.525) (layer Dwgs.User) (width 0.12))
  (fp_line (start {outlineSize} -9.525) (end {outlineSize} 9.525) (layer Dwgs.User) (width 0.12))
  (fp_line (start -{outlineSize} -9.525) (end {outlineSize} -9.525) (layer Dwgs.User) (width 0.12))
  (pad "" np_thru_hole circle (at 0 0) (size 4 4) (drill 4) (layers *.Cu *.Mask))""",

  "Pins": """
  (pad 1 thru_hole circle (at -3.81 -2.54) (size 2.2 2.2) (drill 1.5) (layers *.Cu *.Mask))
  (pad 2 thru_hole circle (at 2.54 -5.08) (size 2.2 2.2) (drill 1.5) (layers *.Cu *.Mask))""",

  "PCB": """
  (pad "" np_thru_hole circle (at -5.08 0) (size 1.75 1.75) (drill 1.75) (layers *.Cu *.Mask))
  (pad "" np_thru_hole circle (at 5.08 0) (size 1.75 1.75) (drill 1.75) (layers *.Cu *.Mask))""",

  "KailhSocket": """
  (pad "" np_thru_hole circle (at -3.81 -2.54) (size 3 3) (drill 3) (layers *.Cu *.Mask))
  (pad "" np_thru_hole circle (at 2.54 -5.08) (size 3 3) (drill 3) (layers *.Cu *.Mask))
  (pad 1 smd rect (at -7.41 -2.54) (size 2.55 2.5) (layers B.Cu B.Paste B.Mask))
  (pad 2 smd rect (at 6.015 -5.08) (size 2.55 2.5) (layers B.Cu B.Paste B.Mask))
  (model "${{KIPRJMOD}}/models/KailhSocket.stp"
    (offset (xyz -0.6 3.8 -3.5))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 180))
  )""",

  "LED": """
  (pad 3 thru_hole circle (at -1.27 5.08) (size 1.6906 1.6906) (drill 0.9906) (layers *.Cu *.Mask))
  (pad 4 thru_hole circle (at 1.27 5.08) (size 1.6906 1.6906) (drill 0.9906) (layers *.Cu *.Mask))""",

  "LTST-A683CEGBW": """
  (fp_line (start -1.7 3.25) (end -2 3.25) (layer B.SilkS) (width 0.12))
  (fp_line (start -2 3.25) (end -2 3.55) (layer B.SilkS) (width 0.12))
  (fp_line (start -1.7 3.55) (end 1.7 3.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start 1.7 3.55) (end 1.7 6.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start 1.7 6.55) (end -1.7 6.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start -1.7 6.55) (end -1.7 3.55) (layer Edge.Cuts) (width 0.05))
  (pad 3 smd rect (at -2.6 4.3) (size 1.8 0.9) (layers B.Cu B.Paste B.Mask))
  (pad 4 smd rect (at -2.6 5.8) (size 1.8 0.9) (layers B.Cu B.Paste B.Mask))
  (pad 5 smd rect (at 2.6 4.3) (size 1.8 0.9) (layers B.Cu B.Paste B.Mask))
  (pad 6 smd rect (at 2.6 5.8) (size 1.8 0.9) (layers B.Cu B.Paste B.Mask))
  (model "${{KIPRJMOD}}/models/LTST-A683CEGBW.step"
    (offset (xyz 0 -5.05 -1.87))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 0))
  )""",

    "SK6812Mini-E": """
  (fp_text reference REF** (at -7.2 7.15) (layer F.SilkS) hide
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value MX_SK6812MINI-E_REV (at -0.65 8.55) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_line (start -0.794452 3.58) (end 0.794452 3.58) (layer Edge.Cuts) (width 0.1))
  (fp_line (start -1.699999 5.782842) (end -1.699999 4.377158) (layer Edge.Cuts) (width 0.1))
  (fp_line (start 0.794452 6.579999) (end -0.794453 6.579999) (layer Edge.Cuts) (width 0.1))
  (fp_line (start 1.699999 4.377158) (end 1.699999 5.782842) (layer Edge.Cuts) (width 0.1))
  (fp_poly (pts (xy -4.2 4.08) (xy -3.3 3.18) (xy -4.2 3.18)) (layer B.SilkS) (width 0.1))
  (fp_line (start -1.6 4.18) (end -1.1 3.68) (layer Dwgs.User) (width 0.12))
  (fp_line (start -1.6 4.18) (end -1.6 6.48) (layer Dwgs.User) (width 0.12))
  (fp_line (start 1.6 3.68) (end -1.1 3.68) (layer Dwgs.User) (width 0.12))
  (fp_line (start 1.6 6.48) (end 1.6 3.68) (layer Dwgs.User) (width 0.12))
  (fp_line (start -1.6 6.48) (end 1.6 6.48) (layer Dwgs.User) (width 0.12))
  (fp_line (start 3.8 7.08) (end 3.8 3.08) (layer B.CrtYd) (width 0.05))
  (fp_line (start 3.8 3.08) (end -3.8 3.08) (layer B.CrtYd) (width 0.05))
  (fp_line (start -3.8 3.08) (end -3.8 7.08) (layer B.CrtYd) (width 0.05))
  (fp_line (start -3.8 7.08) (end 3.8 7.08) (layer B.CrtYd) (width 0.05))
  (fp_line (start -9.525 9.525) (end -9.525 -9.525) (layer Dwgs.User) (width 0.15))
  (fp_line (start 9.525 9.525) (end -9.525 9.525) (layer Dwgs.User) (width 0.15))
  (fp_line (start 9.525 -9.525) (end 9.525 9.525) (layer Dwgs.User) (width 0.15))
  (fp_line (start -9.525 -9.525) (end 9.525 -9.525) (layer Dwgs.User) (width 0.15))
  (fp_text user 1 (at 2.5 7.08 90) (layer B.SilkS) hide
    (effects (font (size 1 1) (thickness 0.15)) (justify mirror))
  )
  (fp_arc (start 1.298969 3.943403) (end 1.749484 4.16028) (angle -146.0053744) (layer Edge.Cuts) (width 0.1))
  (fp_arc (start 2.199999 4.377158) (end 1.749484 4.16028) (angle -25.70611205) (layer Edge.Cuts) (width 0.1))
  (fp_arc (start 2.199999 5.782842) (end 1.699999 5.782842) (angle -25.70611954) (layer Edge.Cuts) (width 0.1))
  (fp_arc (start 1.298969 6.216598) (end 1.046711 6.648299) (angle -146.0054017) (layer Edge.Cuts) (width 0.1))
  (fp_arc (start 0.794452 7.079999) (end 1.046711 6.648299) (angle -30.29928212) (layer Edge.Cuts) (width 0.1))
  (fp_arc (start -0.794453 7.079999) (end -0.794453 6.579999) (angle -30.29922831) (layer Edge.Cuts) (width 0.1))
  (fp_arc (start -1.298969 6.216597) (end -1.749484 5.99972) (angle -146.0053097) (layer Edge.Cuts) (width 0.1))
  (fp_arc (start -2.199999 5.782842) (end -1.749484 5.99972) (angle -25.70608136) (layer Edge.Cuts) (width 0.1))
  (fp_arc (start -2.199999 4.377158) (end -1.699999 4.377158) (angle -25.70617777) (layer Edge.Cuts) (width 0.1))
  (fp_arc (start -1.298969 3.943402) (end -1.046711 3.511701) (angle -146.0055121) (layer Edge.Cuts) (width 0.1))
  (fp_arc (start -0.794452 3.08) (end -1.046711 3.511701) (angle -30.29933433) (layer Edge.Cuts) (width 0.1))
  (fp_arc (start 0.794452 3.08) (end 0.794452 3.58) (angle -30.2992623) (layer Edge.Cuts) (width 0.1))
  (pad 3 smd roundrect (at 2.6 5.83 90) (size 0.82 1.6) (layers B.Cu B.Paste B.Mask) (roundrect_rratio 0.1))
  (pad 4 smd roundrect (at 2.6 4.33 90) (size 0.82 1.6) (layers B.Cu B.Paste B.Mask) (roundrect_rratio 0.1))
  (pad 5 smd roundrect (at -2.6 5.83 90) (size 0.82 1.6) (layers B.Cu B.Paste B.Mask) (roundrect_rratio 0.1))
  (pad 6 smd roundrect (at -2.6 4.33 90) (size 0.82 1.6) (layers B.Cu B.Paste B.Mask) (roundrect_rratio 0.1))
  )""",

  "LTST-A683CEGBW-HS": """
  (fp_line (start -1.7 3.25) (end -2 3.25) (layer B.SilkS) (width 0.12))
  (fp_line (start -2 3.25) (end -2 3.55) (layer B.SilkS) (width 0.12))
  (fp_line (start -1.7 3.55) (end 1.7 3.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start 1.7 3.55) (end 1.7 6.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start 1.7 6.55) (end -1.7 6.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start -1.7 6.55) (end -1.7 3.55) (layer Edge.Cuts) (width 0.05))
  (pad 3 smd rect (at -2.95 4.1) (size 2.5 1.1) (layers B.Cu B.Paste B.Mask))
  (pad 4 smd rect (at -2.95 6) (size 2.5 1.1) (layers B.Cu B.Paste B.Mask))
  (pad 5 smd rect (at 2.95 4.1) (size 2.5 1.1) (layers B.Cu B.Paste B.Mask))
  (pad 6 smd rect (at 2.95 6) (size 2.5 1.1) (layers B.Cu B.Paste B.Mask))
  (model "${{KIPRJMOD}}/models/LTST-A683CEGBW.step"
    (offset (xyz 0 -5.05 -1.87))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 0))
  )""",

  "LTST-A683CEGBW-Rotated": """
  (fp_line (start 1.7 6.85) (end 2 6.85) (layer B.SilkS) (width 0.12))
  (fp_line (start 2 6.85) (end 2 6.55) (layer B.SilkS) (width 0.12))
  (fp_line (start -1.7 3.55) (end 1.7 3.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start 1.7 3.55) (end 1.7 6.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start 1.7 6.55) (end -1.7 6.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start -1.7 6.55) (end -1.7 3.55) (layer Edge.Cuts) (width 0.05))
  (pad 6 smd rect (at -2.6 4.3) (size 1.8 0.9) (layers B.Cu B.Paste B.Mask))
  (pad 5 smd rect (at -2.6 5.8) (size 1.8 0.9) (layers B.Cu B.Paste B.Mask))
  (pad 4 smd rect (at 2.6 4.3) (size 1.8 0.9) (layers B.Cu B.Paste B.Mask))
  (pad 3 smd rect (at 2.6 5.8) (size 1.8 0.9) (layers B.Cu B.Paste B.Mask))
  (model "${{KIPRJMOD}}/models/LTST-A683CEGBW.step"
    (offset (xyz 0 -5.05 -1.87))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 180))
  )""",

  "LTST-A683CEGBW-Rotated-HS": """
  (fp_line (start 1.7 6.85) (end 2 6.85) (layer B.SilkS) (width 0.12))
  (fp_line (start 2 6.85) (end 2 6.55) (layer B.SilkS) (width 0.12))
  (fp_line (start -1.7 3.55) (end 1.7 3.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start 1.7 3.55) (end 1.7 6.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start 1.7 6.55) (end -1.7 6.55) (layer Edge.Cuts) (width 0.05))
  (fp_line (start -1.7 6.55) (end -1.7 3.55) (layer Edge.Cuts) (width 0.05))
  (pad 6 smd rect (at -2.95 4.1) (size 2.5 1.1) (layers B.Cu B.Paste B.Mask))
  (pad 5 smd rect (at -2.95 6) (size 2.5 1.1) (layers B.Cu B.Paste B.Mask))
  (pad 4 smd rect (at 2.95 4.1) (size 2.5 1.1) (layers B.Cu B.Paste B.Mask))
  (pad 3 smd rect (at 2.95 6) (size 2.5 1.1) (layers B.Cu B.Paste B.Mask))
  (model "${{KIPRJMOD}}/models/LTST-A683CEGBW.step"
    (offset (xyz 0 -5.05 -1.87))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 180))
  )""",

  "StabWireTop": """
  (pad "" np_thru_hole circle (at -{stabSpacing} 7) (size 3.05 3.05) (drill 3.05) (layers *.Cu *.Mask))
  (pad "" np_thru_hole circle (at -{stabSpacing} -8.24) (size 4 4) (drill 4) (layers *.Cu *.Mask))
  (pad "" np_thru_hole circle (at {stabSpacing} -8.24) (size 4 4) (drill 4) (layers *.Cu *.Mask))
  (pad "" np_thru_hole circle (at {stabSpacing} 7) (size 3.05 3.05) (drill 3.05) (layers *.Cu *.Mask))""",

  "StabWireBottom": """
  (pad "" np_thru_hole circle (at -{stabSpacing} -7) (size 3.05 3.05) (drill 3.05) (layers *.Cu *.Mask))
  (pad "" np_thru_hole circle (at -{stabSpacing} 8.24) (size 4 4) (drill 4) (layers *.Cu *.Mask))
  (pad "" np_thru_hole circle (at {stabSpacing} 8.24) (size 4 4) (drill 4) (layers *.Cu *.Mask))
  (pad "" np_thru_hole circle (at {stabSpacing} -7) (size 3.05 3.05) (drill 3.05) (layers *.Cu *.Mask))""",

  "BaseEnd": """
)"""
}

variants = [
  [None, "PCB"],
  ["Pins", "KailhSocket"],
  #[None, "StabWireTop", "StabWireBottom"],
  #[None, "LED", "LTST-A683CEGBW", "LTST-A683CEGBW-Rotated", "LTST-A683CEGBW-HS", "LTST-A683CEGBW-Rotated-HS"],
  [None, "PCB","KailhSocket", "SK6812Mini-E"],
]

def generateFootprints():
  for variant in itertools.product(*variants):
    # Filter None values
    components = [component for component in variant if component is not None]

    # Create directory containing all sizes of given variant
    dirname = f"CherryMX_{'_'.join(components)}.pretty".replace("_Pins", "")
    os.makedirs(dirname, exist_ok = True)

    for size in sizesToGenerate:
      if size not in stabSpacings and ("StabWireTop" in components or "StabWireBottom" in components):
        continue

      name = f"CherryMX_{size}u_{'_'.join(components)}".replace("_Pins", "")

      # Generate description
      mountType = "PCB" if "PCB" in components else "Plate"

      usingKailhSocket = "yes" if "KailhSocket" in components else "no"

      stabilizer = (
        "n/a" if float(size) < 2 else (
          "PCB mounted (Wire Top)" if "StabWireTop" in components else (
            "PCB mounted (Wire Bottom)" if "StabWireBottom" in components else "Plate mounted"
          )
        )
      )
      
      lighting = "none"
      lightingMap = {
        "LTST-A683CEGBW": "LTST-A683CEGBW",
        "LTST-A683CEGBW-Rotated": "LTST-A683CEGBW (rotated)",
        "LTST-A683CEGBW-HS": "LTST-A683CEGBW for hand-soldering",
        "LTST-A683CEGBW-Rotated-HS": "LTST-A683CEGBW (rotated) for hand-soldering",
        "LED": "2 pin LED"
      }
      
      for component in components:
        if component in lightingMap:
          lighting = lightingMap[component]
          break

      description = "Cherry MX switch footprint. "
      description += f"Size: {size}u"
      description += f", Mount type: {mountType}"
      description += f", Using Kailh Socket: {usingKailhSocket}"
      description += f", Stabilizer: {stabilizer}"
      description += f", Lighting: {lighting}"

      keywords = name.replace("_", " ")

      # Generate output code
      code = ""
      for component in ["BaseStart", *components, "BaseEnd"]:
        code += componentsList[component].format(
          name=name, 
          description=description, 
          keywords=keywords, 
          outlineSize=float(size) * unit / 2, 
          stabSpacing=stabSpacings[size] / 2 if size in stabSpacings else "",
        )

      # Save footprint to file
      file = open(f"{dirname}/{name}.kicad_mod", "w+")
      file.writelines(code)
      file.close()

      print(f"Generated: {name}.kicad_mod")

generateFootprints()