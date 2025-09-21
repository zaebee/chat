/**
 * Hive Interactive Navigation Enhancement
 * Adapted from medicine.git patterns for Sacred Team documentation
 * Provides bilingual support, dynamic navigation, and visual enhancements
 */

class HiveDocumentationEnhancer {
    constructor() {
        this.currentLanguage = this.detectLanguage();
        this.glossary = {};
        this.navigationTree = {};
        this.searchIndex = {};
        this.sacredTeamTheme = {
            primary: '#FFD700',    // Sacred gold
            secondary: '#8B4513',  // Sacred brown
            accent: '#FF6B35',     // Sacred orange
            background: '#FFF8DC', // Sacred cream
            text: '#2F4F4F'        // Sacred dark slate
        };
        
        this.init();
    }
    
    async init() {
        console.log('🐝 Initializing Hive Documentation Enhancer');
        
        try {
            await this.loadGlossary();
            this.initializeLanguageSwitching();
            this.enhanceNavigation();
            this.addVisualPatterns();
            this.initializeSearch();
            this.addSacredTeamTheming();
            this.initializeResponsiveDesign();
            
            console.log('✅ Hive Documentation Enhancement Complete');
        } catch (error) {
            console.error('❌ Enhancement initialization failed:', error);
        }
    }
    
    detectLanguage() {
        // Detect language from URL, localStorage, or browser
        const urlLang = new URLSearchParams(window.location.search).get('lang');
        const storedLang = localStorage.getItem('hive_language');
        const browserLang = navigator.language.startsWith('ru') ? 'ru' : 'en';
        
        return urlLang || storedLang || browserLang;
    }
    
    async loadGlossary() {
        try {
            // In Jekyll, this would be injected via liquid template
            // For now, we'll use a placeholder structure
            this.glossary = window.hiveGlossary || {};
            console.log('📚 Glossary loaded:', Object.keys(this.glossary).length, 'categories');
        } catch (error) {
            console.warn('⚠️ Could not load glossary:', error);
        }
    }
    
    initializeLanguageSwitching() {
        // Create language switcher
        const languageSwitcher = this.createLanguageSwitcher();
        
        // Add to header or navigation
        const header = document.querySelector('header') || document.querySelector('nav') || document.body;
        if (header) {
            header.appendChild(languageSwitcher);
        }
        
        // Apply current language
        this.applyLanguage(this.currentLanguage);
    }
    
    createLanguageSwitcher() {
        const switcher = document.createElement('div');
        switcher.className = 'hive-language-switcher';
        switcher.innerHTML = `
            <div class="language-toggle">
                <button class="lang-btn ${this.currentLanguage === 'en' ? 'active' : ''}" 
                        data-lang="en" title="English">EN</button>
                <button class="lang-btn ${this.currentLanguage === 'ru' ? 'active' : ''}" 
                        data-lang="ru" title="Русский">RU</button>
            </div>
        `;
        
        // Add event listeners
        switcher.querySelectorAll('.lang-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const newLang = e.target.dataset.lang;
                this.switchLanguage(newLang);
            });
        });
        
        return switcher;
    }
    
    switchLanguage(newLang) {
        if (newLang === this.currentLanguage) return;
        
        this.currentLanguage = newLang;
        localStorage.setItem('hive_language', newLang);
        
        // Update active button
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === newLang);
        });
        
        // Apply language changes
        this.applyLanguage(newLang);
        
        // Update URL without reload
        const url = new URL(window.location);
        url.searchParams.set('lang', newLang);
        window.history.replaceState({}, '', url);
        
        console.log(`🌐 Language switched to: ${newLang}`);
    }
    
    applyLanguage(lang) {
        // Apply translations to elements with data-translate attributes
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.dataset.translate;
            const translation = this.getTranslation(key, lang);
            if (translation) {
                element.textContent = translation;
            }
        });
        
        // Update document language attribute
        document.documentElement.lang = lang;
    }
    
    getTranslation(key, lang = this.currentLanguage) {
        // Navigate nested glossary structure: category.term.language
        const parts = key.split('.');
        let current = this.glossary;
        
        for (const part of parts) {
            if (current && current[part]) {
                current = current[part];
            } else {
                return null;
            }
        }
        
        return current && current[lang] ? current[lang] : null;
    }
    
    enhanceNavigation() {
        // Create enhanced navigation with Sacred Team styling
        this.createSacredNavigation();
        this.addNavigationInteractivity();
        this.createBreadcrumbs();
    }
    
    createSacredNavigation() {
        const nav = document.querySelector('nav') || this.createNavigationContainer();
        
        // Add Sacred Team navigation structure
        const sacredNav = document.createElement('div');
        sacredNav.className = 'sacred-navigation';
        sacredNav.innerHTML = `
            <div class="nav-section" data-section="foundation">
                <h3 data-translate="ui.foundation">Foundation</h3>
                <ul class="nav-links">
                    <li><a href="/docs/00_FOUNDATION/" data-translate="ui.getting_started">Getting Started</a></li>
                    <li><a href="/docs/01_ARCHITECTURE/" data-translate="ui.architecture">Architecture</a></li>
                </ul>
            </div>
            <div class="nav-section" data-section="development">
                <h3 data-translate="ui.development">Development</h3>
                <ul class="nav-links">
                    <li><a href="/docs/02_DEVELOPMENT/" data-translate="development.setup">Setup</a></li>
                    <li><a href="/docs/03_API/" data-translate="ui.api_reference">API Reference</a></li>
                </ul>
            </div>
            <div class="nav-section" data-section="sacred-team">
                <h3 data-translate="ui.sacred_chronicles">Sacred Chronicles</h3>
                <ul class="nav-links">
                    <li><a href="/docs/sacred-team/" data-translate="ui.team_coordination">Team Coordination</a></li>
                    <li><a href="/docs/sacred-team/chronicles/" data-translate="ui.sacred_chronicles">Chronicles</a></li>
                </ul>
            </div>
        `;
        
        nav.appendChild(sacredNav);
    }
    
    createNavigationContainer() {
        const nav = document.createElement('nav');
        nav.className = 'hive-navigation';
        document.body.insertBefore(nav, document.body.firstChild);
        return nav;
    }
    
    addNavigationInteractivity() {
        // Collapsible sections
        document.querySelectorAll('.nav-section h3').forEach(header => {
            header.addEventListener('click', () => {
                const section = header.parentElement;
                section.classList.toggle('collapsed');
            });
        });
        
        // Highlight current page
        const currentPath = window.location.pathname;
        document.querySelectorAll('.nav-links a').forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('current');
            }
        });
    }
    
    createBreadcrumbs() {
        const breadcrumbs = document.createElement('nav');
        breadcrumbs.className = 'hive-breadcrumbs';
        breadcrumbs.setAttribute('aria-label', 'Breadcrumb');
        
        const pathParts = window.location.pathname.split('/').filter(part => part);
        const breadcrumbItems = ['Home'];
        
        // Build breadcrumb path
        let currentPath = '';
        pathParts.forEach(part => {
            currentPath += '/' + part;
            breadcrumbItems.push(this.formatBreadcrumbItem(part));
        });
        
        breadcrumbs.innerHTML = `
            <ol class="breadcrumb-list">
                ${breadcrumbItems.map((item, index) => `
                    <li class="breadcrumb-item ${index === breadcrumbItems.length - 1 ? 'current' : ''}">
                        ${index === breadcrumbItems.length - 1 ? item : `<a href="#">${item}</a>`}
                    </li>
                `).join('')}
            </ol>
        `;
        
        // Insert breadcrumbs after navigation
        const nav = document.querySelector('.hive-navigation');
        if (nav && nav.nextSibling) {
            nav.parentNode.insertBefore(breadcrumbs, nav.nextSibling);
        }
    }
    
    formatBreadcrumbItem(pathPart) {
        // Convert path parts to readable names
        const formatMap = {
            'docs': 'Documentation',
            'sacred-team': 'Sacred Team',
            'chronicles': 'Chronicles',
            'coordination': 'Coordination'
        };
        
        return formatMap[pathPart] || pathPart.replace(/[-_]/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase());
    }
    
    addVisualPatterns() {
        // Enhance Mermaid diagrams with Sacred Team theming
        this.enhanceMermaidDiagrams();
        
        // Add visual indicators for different content types
        this.addContentTypeIndicators();
        
        // Add Sacred Team visual elements
        this.addSacredVisualElements();
    }
    
    enhanceMermaidDiagrams() {
        // Wait for Mermaid to load, then apply Sacred Team theme
        if (typeof mermaid !== 'undefined') {
            mermaid.initialize({
                theme: 'base',
                themeVariables: {
                    primaryColor: this.sacredTeamTheme.primary,
                    primaryTextColor: this.sacredTeamTheme.text,
                    primaryBorderColor: this.sacredTeamTheme.secondary,
                    lineColor: this.sacredTeamTheme.accent,
                    secondaryColor: this.sacredTeamTheme.background,
                    tertiaryColor: this.sacredTeamTheme.accent
                }
            });
        }
        
        // Add click-to-navigate functionality to diagrams
        document.querySelectorAll('.mermaid').forEach(diagram => {
            diagram.addEventListener('click', (e) => {
                // Handle diagram navigation
                this.handleDiagramNavigation(e);
            });
        });
    }
    
    handleDiagramNavigation(event) {
        // Extract navigation hints from clicked diagram elements
        const target = event.target;
        const nodeText = target.textContent;
        
        // Simple navigation mapping
        const navigationMap = {
            'ATCG': '/docs/01_ARCHITECTURE/',
            'Pollen Protocol': '/docs/03_API/',
            'Sacred Team': '/docs/sacred-team/',
            'bee.chronicler': '/docs/sacred-team/chronicles/'
        };
        
        if (navigationMap[nodeText]) {
            window.location.href = navigationMap[nodeText];
        }
    }
    
    addContentTypeIndicators() {
        // Add visual indicators for different types of content
        document.querySelectorAll('h1, h2, h3').forEach(heading => {
            const text = heading.textContent.toLowerCase();
            
            if (text.includes('api') || text.includes('reference')) {
                heading.classList.add('api-heading');
                heading.insertAdjacentHTML('afterbegin', '<span class=\"content-icon\">🔧</span> ');
            } else if (text.includes('sacred') || text.includes('team')) {
                heading.classList.add('sacred-heading');
                heading.insertAdjacentHTML('afterbegin', '<span class=\"content-icon\">🐝</span> ');
            } else if (text.includes('guide') || text.includes('tutorial')) {
                heading.classList.add('guide-heading');
                heading.insertAdjacentHTML('afterbegin', '<span class=\"content-icon\">📚</span> ');
            }
        });
    }
    
    addSacredVisualElements() {
        // Add Sacred Team visual flourishes
        const body = document.body;
        body.classList.add('sacred-theme');
        
        // Add sacred patterns to page corners
        const corners = ['top-left', 'top-right', 'bottom-left', 'bottom-right'];
        corners.forEach(corner => {
            const element = document.createElement('div');
            element.className = `sacred-corner ${corner}`;
            element.innerHTML = '🌟';
            body.appendChild(element);
        });
    }
    
    initializeSearch() {
        // Create search functionality
        const searchContainer = this.createSearchContainer();
        
        // Add to navigation
        const nav = document.querySelector('.hive-navigation');
        if (nav) {
            nav.insertBefore(searchContainer, nav.firstChild);
        }
        
        // Build search index
        this.buildSearchIndex();
    }
    
    createSearchContainer() {
        const container = document.createElement('div');
        container.className = 'hive-search';
        container.innerHTML = `
            <div class="search-box">
                <input type="text" 
                       class="search-input" 
                       placeholder="${this.getTranslation('ui.search') || 'Search...'}"
                       aria-label="Search documentation">
                <button class="search-button" aria-label="Search">
                    <span class="search-icon">🔍</span>
                </button>
            </div>
            <div class="search-results" style="display: none;"></div>
        `;
        
        // Add search functionality
        const input = container.querySelector('.search-input');
        const results = container.querySelector('.search-results');
        
        input.addEventListener('input', (e) => {
            this.performSearch(e.target.value, results);
        });
        
        return container;
    }
    
    buildSearchIndex() {
        // Build search index from page content
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        const paragraphs = document.querySelectorAll('p');
        
        this.searchIndex = {
            headings: Array.from(headings).map(h => ({
                text: h.textContent,
                level: h.tagName,
                element: h
            })),
            content: Array.from(paragraphs).map(p => ({
                text: p.textContent,
                element: p
            }))
        };
    }
    
    performSearch(query, resultsContainer) {
        if (!query || query.length < 2) {
            resultsContainer.style.display = 'none';
            return;
        }
        
        const results = [];
        const queryLower = query.toLowerCase();
        
        // Search headings
        this.searchIndex.headings.forEach(item => {
            if (item.text.toLowerCase().includes(queryLower)) {
                results.push({
                    type: 'heading',
                    text: item.text,
                    element: item.element
                });
            }
        });
        
        // Search content
        this.searchIndex.content.forEach(item => {
            if (item.text.toLowerCase().includes(queryLower)) {
                results.push({
                    type: 'content',
                    text: item.text.substring(0, 100) + '...',
                    element: item.element
                });
            }
        });
        
        this.displaySearchResults(results, resultsContainer);
    }
    
    displaySearchResults(results, container) {
        if (results.length === 0) {
            container.innerHTML = '<div class=\"no-results\">No results found</div>';
        } else {
            container.innerHTML = results.map(result => `
                <div class="search-result" data-type="${result.type}">
                    <div class="result-text">${result.text}</div>
                </div>
            `).join('');
            
            // Add click handlers
            container.querySelectorAll('.search-result').forEach((resultEl, index) => {
                resultEl.addEventListener('click', () => {
                    results[index].element.scrollIntoView({ behavior: 'smooth' });
                    container.style.display = 'none';
                });
            });
        }
        
        container.style.display = 'block';
    }
    
    addSacredTeamTheming() {
        // Inject Sacred Team CSS
        const style = document.createElement('style');
        style.textContent = this.getSacredTeamCSS();
        document.head.appendChild(style);
    }
    
    getSacredTeamCSS() {
        return `
            /* Sacred Team Theme */
            .sacred-theme {
                --sacred-primary: ${this.sacredTeamTheme.primary};
                --sacred-secondary: ${this.sacredTeamTheme.secondary};
                --sacred-accent: ${this.sacredTeamTheme.accent};
                --sacred-background: ${this.sacredTeamTheme.background};
                --sacred-text: ${this.sacredTeamTheme.text};
            }
            
            .hive-language-switcher {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 1000;
            }
            
            .language-toggle {
                display: flex;
                background: var(--sacred-background);
                border-radius: 20px;
                padding: 5px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .lang-btn {
                padding: 8px 16px;
                border: none;
                background: transparent;
                border-radius: 15px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: bold;
                color: var(--sacred-text);
            }
            
            .lang-btn.active {
                background: var(--sacred-primary);
                color: var(--sacred-secondary);
            }
            
            .sacred-navigation {
                background: var(--sacred-background);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            .nav-section h3 {
                color: var(--sacred-secondary);
                cursor: pointer;
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }
            
            .nav-section h3:before {
                content: '🐝';
                margin-right: 8px;
            }
            
            .nav-links a {
                color: var(--sacred-text);
                text-decoration: none;
                padding: 5px 0;
                display: block;
                transition: color 0.3s ease;
            }
            
            .nav-links a:hover,
            .nav-links a.current {
                color: var(--sacred-accent);
                font-weight: bold;
            }
            
            .hive-search {
                margin-bottom: 20px;
            }
            
            .search-box {
                display: flex;
                background: white;
                border-radius: 25px;
                padding: 5px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .search-input {
                flex: 1;
                border: none;
                padding: 10px 15px;
                border-radius: 20px;
                outline: none;
            }
            
            .search-button {
                background: var(--sacred-primary);
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .search-results {
                background: white;
                border-radius: 10px;
                margin-top: 5px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                max-height: 300px;
                overflow-y: auto;
            }
            
            .search-result {
                padding: 10px 15px;
                cursor: pointer;
                border-bottom: 1px solid #eee;
            }
            
            .search-result:hover {
                background: var(--sacred-background);
            }
            
            .sacred-corner {
                position: fixed;
                font-size: 20px;
                z-index: 999;
                opacity: 0.3;
                pointer-events: none;
            }
            
            .sacred-corner.top-left { top: 10px; left: 10px; }
            .sacred-corner.top-right { top: 10px; right: 10px; }
            .sacred-corner.bottom-left { bottom: 10px; left: 10px; }
            .sacred-corner.bottom-right { bottom: 10px; right: 10px; }
            
            .content-icon {
                margin-right: 8px;
            }
            
            .api-heading { border-left: 4px solid var(--sacred-accent); padding-left: 10px; }
            .sacred-heading { border-left: 4px solid var(--sacred-primary); padding-left: 10px; }
            .guide-heading { border-left: 4px solid var(--sacred-secondary); padding-left: 10px; }
            
            .hive-breadcrumbs {
                margin: 10px 0;
                padding: 10px;
                background: rgba(255, 215, 0, 0.1);
                border-radius: 5px;
            }
            
            .breadcrumb-list {
                display: flex;
                list-style: none;
                padding: 0;
                margin: 0;
            }
            
            .breadcrumb-item:not(:last-child):after {
                content: ' / ';
                margin: 0 8px;
                color: var(--sacred-secondary);
            }
            
            .breadcrumb-item.current {
                font-weight: bold;
                color: var(--sacred-accent);
            }
        `;
    }
    
    initializeResponsiveDesign() {
        // Add responsive behavior
        this.handleResponsiveNavigation();
        this.addMobileOptimizations();
    }
    
    handleResponsiveNavigation() {
        // Create mobile menu toggle
        const mobileToggle = document.createElement('button');
        mobileToggle.className = 'mobile-nav-toggle';
        mobileToggle.innerHTML = '☰';
        mobileToggle.setAttribute('aria-label', 'Toggle navigation');
        
        const nav = document.querySelector('.hive-navigation');
        if (nav) {
            nav.insertBefore(mobileToggle, nav.firstChild);
            
            mobileToggle.addEventListener('click', () => {
                nav.classList.toggle('mobile-open');
            });
        }
    }
    
    addMobileOptimizations() {
        // Add mobile-specific CSS
        const mobileStyle = document.createElement('style');
        mobileStyle.textContent = `
            @media (max-width: 768px) {
                .hive-language-switcher {
                    position: relative;
                    top: auto;
                    right: auto;
                    margin-bottom: 10px;
                }
                
                .sacred-navigation {
                    display: none;
                }
                
                .sacred-navigation.mobile-open {
                    display: block;
                }
                
                .mobile-nav-toggle {
                    display: block;
                    background: var(--sacred-primary);
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 18px;
                    cursor: pointer;
                    margin-bottom: 10px;
                }
                
                .sacred-corner {
                    display: none;
                }
            }
            
            @media (min-width: 769px) {
                .mobile-nav-toggle {
                    display: none;
                }
            }
        `;
        document.head.appendChild(mobileStyle);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new HiveDocumentationEnhancer();
    });
} else {
    new HiveDocumentationEnhancer();
}

// Export for potential external use
window.HiveDocumentationEnhancer = HiveDocumentationEnhancer;