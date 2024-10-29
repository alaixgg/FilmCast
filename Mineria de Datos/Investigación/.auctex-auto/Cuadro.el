;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "Cuadro"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("scrartcl" "")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("amsmath" "") ("amsthm" "") ("amssymb" "") ("amsfonts" "") ("thmtools" "") ("graphicx" "") ("setspace" "") ("geometry" "") ("float" "") ("hyperref" "hidelinks") ("inputenc" "utf8") ("babel" "spanish") ("framed" "") ("xcolor" "dvipsnames") ("tcolorbox" "") ("tikz" "") ("pdflscape" "") ("svg" "") ("subcaption" "") ("multirow" "") ("array" "") ("listings" "") ("supertabular" "") ("tabularx" "") ("longtable" "") ("tabu" "") ("ltablex" "") ("ltxtable" "") ("booktabs" "") ("caption" "") ("apacite" "") ("hhline" "") ("blindtext" "")))
   (TeX-run-style-hooks
    "latex2e"
    "scrartcl"
    "scrartcl10"
    "amsmath"
    "amsthm"
    "amssymb"
    "amsfonts"
    "thmtools"
    "graphicx"
    "setspace"
    "geometry"
    "float"
    "hyperref"
    "inputenc"
    "babel"
    "framed"
    "xcolor"
    "tcolorbox"
    "tikz"
    "caption"
    "longtable"
    "pdflscape"
    "svg"
    "subcaption"
    "multirow"
    "array"
    "listings"
    "supertabular"
    "tabularx"
    "tabu"
    "ltablex"
    "ltxtable"
    "booktabs"
    "apacite"
    "hhline"
    "blindtext")
   (TeX-add-symbols
    '("HRule" 1)
    "newline")
   (LaTeX-add-environments
    '("@IEEEbogusbiography" LaTeX-env-args ["argument"] 1)
    '("IEEEbiography" LaTeX-env-args ["argument"] 1)
    '("subfloatrow*" LaTeX-env-args ["argument"] 0)))
 :latex)

