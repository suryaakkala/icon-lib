import os
import json
import random
from collections import defaultdict

def generate_icon_list():
    # Paths to your icon folders
    png_dir = 'src/icons/png'
    svg_dir = 'src/icons/svg'
    
    # Available categories
    categories = [
        'technology',
        'social',
        'programming',
        'cloud',
        'database',
        'framework',
        'devops',
        'design',
        'hardware',
        'ai',
        'gaming',
        'finance',
        'education',
        'health',
        'entertainment'
    ]
    
    # Special known icons with fixed categories
    known_icons = {
        'docker': 'devops',
        'kubernetes': 'devops',
        'jenkins': 'devops',
        'github': 'social',
        'gitlab': 'social',
        'bitbucket': 'social',
        'twitter': 'social',
        'facebook': 'social',
        'instagram': 'social',
        'python': 'programming',
        'java': 'programming',
        'javascript': 'programming',
        'react': 'framework',
        'vue': 'framework',
        'angular': 'framework',
        'aws': 'cloud',
        'azure': 'cloud',
        'gcp': 'cloud',
        'mysql': 'database',
        'mongodb': 'database',
        'postgresql': 'database',
        'nodejs': 'programming',
        'nginx': 'technology',
        'ubuntu': 'technology',
        'windows': 'technology',
        'apple': 'technology',
        'android': 'technology'
    }
    
    # Weighted random categories (technology-related more likely)
    weighted_categories = random.choices(
        categories,
        weights=[30, 10, 20, 15, 10, 15, 15, 5, 5, 10, 5, 5, 5, 5, 5],
        k=1000
    )
    category_iter = iter(weighted_categories)
    
    icons_data = defaultdict(lambda: {'formats': [], 'category': None})
    
    # Scan PNG files
    for filename in os.listdir(png_dir):
        if filename.endswith('.png'):
            icon_name = os.path.splitext(filename)[0]
            icons_data[icon_name]['formats'].append('png')
    
    # Scan SVG files
    for filename in os.listdir(svg_dir):
        if filename.endswith('.svg'):
            icon_name = os.path.splitext(filename)[0]
            icons_data[icon_name]['formats'].append('svg')
    
    # Assign categories
    icons_list = []
    for name, data in icons_data.items():
        # Use known category if available, otherwise random
        category = known_icons.get(name)
        if not category:
            try:
                category = next(category_iter)
            except StopIteration:
                category = random.choice(categories)
        
        icons_list.append({
            'name': name,
            'formats': sorted(list(set(data['formats']))),
            'category': category
        })
    
    # Sort alphabetically by name
    icons_list.sort(key=lambda x: x['name'])
    
    return icons_list

def save_as_js(icons_list, output_file='src/js/icons.js'):
    js_content = "// Auto-generated icon list\n"
    js_content += "const icons = [\n"
    
    for icon in icons_list:
        js_content += f"    {{ name: '{icon['name']}', formats: {json.dumps(icon['formats'])}, category: '{icon['category']}' }},\n"
    
    js_content += "];\n\nexport default icons;"
    
    with open(output_file, 'w') as f:
        f.write(js_content)
    
    print(f"Generated {output_file} with {len(icons_list)} icons")
    print("Categories distribution:")
    
    # Print category statistics
    from collections import Counter
    categories = [icon['category'] for icon in icons_list]
    for cat, count in Counter(categories).most_common():
        print(f"- {cat}: {count} icons")

if __name__ == "__main__":
    random.seed(42)  # For reproducible results
    icons = generate_icon_list()
    save_as_js(icons)