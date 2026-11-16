drivers = [
    {'name': 'Alex', 'grid': 1, 'finish': 1},
    {'name': 'Bima', 'grid': 2, 'finish': 5},
    {'name': 'Carlo', 'grid': 3, 'finish': 2},
    {'name': 'Dion', 'grid': 4, 'finish': 4},
    {'name': 'Eka', 'grid': 5, 'finish': 3},
]

def points_for_position(position):
    points_table = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
    return points_table.get(position, 0)

for d in drivers:
    name, grid, finish = d['name'], d['grid'], d['finish']
    print(f'{name}: start P{grid} -> finish P{finish} = {points_for_position(finish)} pts')

# manual rule made by a human (future baseline in Session 5)
def predict_podium(grid):
    return grid <= 3

correct = 0
for d in drivers:
    if predict_podium(d['grid']) == (d['finish'] <= 3):
        correct += 1
print(f'Manual rule accuracy: {correct / len(drivers):.0%}')