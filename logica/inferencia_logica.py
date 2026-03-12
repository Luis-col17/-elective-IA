rules = [(["tiene_fiebre", "tiene_tos"], "tiene_gripe"),
        (["tiene_gripe"], "debe_descansar")]

facts= {"tiene_tos", "tiene_fiebre"}

for conds, conl in rules:
    if all(cond in facts for cond in conds):
        facts.add(conl)
print("Hechos deducidos: ", facts)