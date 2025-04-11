import { icons } from './icons.mjs'; // or './icons.mjs'

document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('icons-container');

    function renderIcons(filteredIcons) {
        container.innerHTML = '';
        filteredIcons.forEach(icon => {
            icon.formats.forEach(format => {
                const iconCard = document.createElement('div');
                iconCard.className = 'icon-card';

                const path = `/icons/${format}/${icon.name}.${format}`;
                console.log(`[LOAD] Trying to load: ${path}`);

                const img = document.createElement('img');
                img.src = path;
                img.alt = `${icon.name} ${format} icon`;

                img.onerror = () => console.error(`[ERROR] Failed to load: ${path}`);
                img.onload = () => console.log(`[OK] Loaded: ${path}`);

                const downloadBtn = document.createElement('a');
                downloadBtn.href = path;
                downloadBtn.download = `${icon.name}.${format}`;
                downloadBtn.textContent = `Download ${format.toUpperCase()}`;
                downloadBtn.className = 'download-btn';

                iconCard.appendChild(img);
                iconCard.appendChild(downloadBtn);
                container.appendChild(iconCard);
            });
        });
    }

    renderIcons(icons);

    document.getElementById('search-btn').addEventListener('click', () => {
        const searchTerm = document.getElementById('search').value.toLowerCase();
        const filtered = icons.filter(icon => icon.name.includes(searchTerm));
        console.log(`[SEARCH] ${filtered.length} results for "${searchTerm}"`);
        renderIcons(filtered);
    });

    document.getElementById('format-filter').addEventListener('change', () => {
        const format = document.getElementById('format-filter').value;
        const category = document.getElementById('category-filter').value;

        let filtered = icons;
        if (format !== 'all') {
            filtered = filtered.filter(icon => icon.formats.includes(format));
        }
        if (category !== 'all') {
            filtered = filtered.filter(icon => icon.category === category);
        }

        console.log(`[FILTER] Format: ${format}, Category: ${category}`);
        renderIcons(filtered);
    });

    document.getElementById('category-filter').addEventListener('change', () => {
        document.getElementById('format-filter').dispatchEvent(new Event('change'));
    });
});
