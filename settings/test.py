from kerykeion import AstrologicalSubject, KerykeionChartSVG

first = AstrologicalSubject("Test", 1970, 3, 8, 18, 30, "Manchester", "US")

# Set the type, it can be Natal, Synastry or Transit
synastry_chart = KerykeionChartSVG(first, "Natal")
synastry_chart.makeSVG()