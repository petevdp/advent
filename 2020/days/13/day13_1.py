import sys

filename = sys.argv[1] if len(sys.argv) >= 2 else 'input'

with open(f'days/13/{filename}') as f:
    first, second = f.read().strip().split('\n')
    wait = int(first.strip())
    busses = [int(b) for b in second.strip().split(',') if b != 'x']
    
    
def wait_for_bus(bus):
    return bus - (wait % bus)
    
best_bus = busses[0]
print('wait: ', wait)
print('best bus: ', best_bus, ' ', wait_for_bus(best_bus))
for bus in busses[1:]:
    print('bus: ', bus, ' ', wait_for_bus(bus))
    if wait_for_bus(bus) < wait_for_bus(best_bus):
        best_bus = bus
        print('best bus: ', best_bus)
    
print(best_bus * wait_for_bus(best_bus))
