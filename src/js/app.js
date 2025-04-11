import icons from './icons.json'; // Assuming icons.json is in the same directory

document.addEventListener('DOMContentLoaded', function() {
    // This would be replaced with actual API calls or file system reading
    // For demo purposes, we'll use mock data
    // const icons = [
    //     { name: 'docker', formats: ['png', 'svg'], category: 'technology' },
    //     { name: 'jenkins', formats: ['png', 'svg'], category: 'technology' },
    //     { name: 'github', formats: ['png', 'svg'], category: 'social' },
    //     // ... 997 more icons
    // ];

    const container = document.getElementById('icons-container');
    
    function renderIcons(filteredIcons) {
        container.innerHTML = '';
        filteredIcons.forEach(icon => {
            icon.formats.forEach(format => {
                const iconCard = document.createElement('div');
                iconCard.className = 'icon-card';
                
                const img = document.createElement('img');
                img.src = `/icons/${format}/${icon.name}.${format}`;
                img.alt = `${icon.name} ${format} icon`;
                
                const downloadBtn = document.createElement('a');
                downloadBtn.href = `/icons/${format}/${icon.name}.${format}`;
                downloadBtn.download = `${icon.name}.${format}`;
                downloadBtn.textContent = `Download ${format.toUpperCase()}`;
                downloadBtn.className = 'download-btn';
                
                iconCard.appendChild(img);
                iconCard.appendChild(downloadBtn);
                container.appendChild(iconCard);
            });
        });
    }
    
    // Initial render
    renderIcons(icons);
    
    // Search functionality
    document.getElementById('search-btn').addEventListener('click', function() {
        const searchTerm = document.getElementById('search').value.toLowerCase();
        const filtered = icons.filter(icon => 
            icon.name.includes(searchTerm)
        );
        renderIcons(filtered);
    });
    
    // Filter functionality
    document.getElementById('format-filter').addEventListener('change', function() {
        const format = this.value;
        const category = document.getElementById('category-filter').value;
        
        let filtered = icons;
        if (format !== 'all') {
            filtered = filtered.filter(icon => icon.formats.includes(format));
        }
        if (category !== 'all') {
            filtered = filtered.filter(icon => icon.category === category);
        }
        
        renderIcons(filtered);
    });
    
    document.getElementById('category-filter').addEventListener('change', function() {
        document.getElementById('format-filter').dispatchEvent(new Event('change'));
    });
});