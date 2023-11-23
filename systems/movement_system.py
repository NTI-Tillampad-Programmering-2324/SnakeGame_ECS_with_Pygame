from components import PositionComponent, DirectionComponent

class MovementSystem:
    def update(self, entity):
        pos = entity.components[PositionComponent]
        dir = entity.components.get(DirectionComponent)
        if dir:
            pos.x += dir.dx
            pos.y += dir.dy