import sys
import os

# Add the path to sys.path
sys.path.append('/workspaces/Sneak/src/generator/Model - 2')

try:
    import generator as mapgen
    generator = mapgen.MapGenerator()
    
    # Generate the map
    generator.generateMap()
    
    # Print the map
    generator.printMap()
    print("Module 'generator' imported successfully.")
except ImportError as e:
    print(f"Import error: {e}")
