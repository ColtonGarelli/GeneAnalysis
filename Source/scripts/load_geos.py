from data_processing import parse_geo

geos = ['GSE52471', 'GSE72535', 'GSE81071']
paths = ["/Users/coltongarelli/pyLibraries/GeneAnalysis/GSE52471_family.soft.gz",
         "/Users/coltongarelli/pyLibraries/GeneAnalysis/GSE72535_family.soft.gz",
         "/Users/coltongarelli/pyLibraries/GeneAnalysis/GSE81071_family.soft.gz"]

print(type(parse_geo.get_geo(paths=paths)[0]))
