class CollisionSystem:
    def check_collision(self, snake, food, PositionComponent):
        snake_pos = snake.components[PositionComponent]
        food_pos = food.components[PositionComponent]
        return snake_pos.x == food_pos.x and snake_pos.y == food_pos.y
