from recommender.user_cir_engine import UserCIREngine

engine = UserCIREngine()

# Using previously stored item
item = "item_001.jpg"

result, reason = engine.retrieve(item)

print("Given item:", item)
print("Recommended item:", result)
print("Reason:", reason)
