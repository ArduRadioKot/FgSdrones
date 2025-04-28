// Language management module
const LanguageManager = {
    currentLanguage: 'en',
    
    translations: {
      en: {
        sidebar: {
          products: 'Products',
          simulator: 'Web Simulator',
          unityGame: 'Unity Game',
          ide: 'Drone IDE',
          docs: 'Documentation'
        },
        projects: 'PROJECTS',
        socialMedia: 'Social Media',
        footer: '© 2024 FgSDRONES. All rights reserved.'
      },
      ru: {
        sidebar: {
          products: 'Продукты',
          simulator: 'Веб симулятор',
          unityGame: 'Игра на Unity',
          ide: 'Редактор кода для квадрокоптера',
          docs: 'Документация'
        },
        projects: 'ПРОЕКТЫ',
        socialMedia: 'Социальные сети',
        footer: '© 2024 FgSDRONES. Все права защищены.'
      }
    },
  
    init() {
      this.loadLanguagePreference();
      this.applyLanguage(this.currentLanguage);
    },
  
    loadLanguagePreference() {
      const savedLanguage = localStorage.getItem('fgsdronesLanguage');
      if (savedLanguage) {
        this.currentLanguage = savedLanguage;
      }
    },
  
    toggleLanguage() {
      const newLanguage = this.currentLanguage === 'en' ? 'ru' : 'en';
      this.setLanguage(newLanguage);
    },
  
    setLanguage(lang) {
      this.currentLanguage = lang;
      localStorage.setItem('fgsdronesLanguage', lang);
      this.applyLanguage(lang);
    },
  
    applyLanguage(lang) {
      const translations = this.translations[lang];
      
      // Update sidebar
      document.querySelector('.sidebar-nav a[href="#products"]').innerHTML = 
        `<i class="fas fa-box-open"></i>${translations.sidebar.products}`;
      document.querySelector('.sidebar-nav a[href="sim.html"]').innerHTML = 
        `<i class="fas fa-laptop-code"></i>${translations.sidebar.simulator}`;
      document.querySelector('.sidebar-nav a[href="#progect2"]').innerHTML = 
        `<i class="fas fa-gamepad"></i>${translations.sidebar.unityGame}`;
      document.querySelector('.sidebar-nav a[href="ide.html"]').innerHTML = 
        `<i class="fas fa-code"></i>${translations.sidebar.ide}`;
      document.querySelector('.sidebar-nav a[href="about.html"]').innerHTML = 
        `<i class="fas fa-file-alt"></i>${translations.sidebar.docs}`;
      
      // Update other elements
      document.querySelector('.language-toggle').innerHTML = 
        `<i class="fas fa-language"></i> ${lang === 'en' ? 'Русский' : 'English'}`;
      
      document.querySelector('.projects-section .section-title h2').textContent = 
        translations.projects;
      
      document.querySelector('.socialmedia-section h2').textContent = 
        translations.socialMedia;
      
      document.querySelector('.copyright').innerHTML = 
        `&copy; 2024 FgSDRONES. ${lang === 'en' ? 'All rights reserved.' : 'Все права защищены.'}`;
    }
  };
  
  // UI Controls module
  const UIControls = {
    init() {
      this.setupEventListeners();
    },
  
    setupEventListeners() {
      // Sidebar controls
      document.querySelector('.menu-icon').addEventListener('click', this.openNav);
      document.querySelector('.closebtn').addEventListener('click', this.closeNav);
      
      // Language toggle
      document.querySelector('.language-toggle').addEventListener('click', () => {
        LanguageManager.toggleLanguage();
      });
      
      // Close sidebar when clicking outside
      document.addEventListener('click', (event) => {
        const sidebar = document.getElementById('mySidebar');
        const menuIcon = document.querySelector('.menu-icon');
        
        if (!sidebar.contains(event.target) && event.target !== menuIcon && !menuIcon.contains(event.target)) {
          this.closeNav();
        }
      });
      
      // Smooth scrolling for anchor links
      document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
          e.preventDefault();
          
          const targetId = this.getAttribute('href');
          if (targetId === '#') return;
          
          const targetElement = document.querySelector(targetId);
          if (targetElement) {
            window.scrollTo({
              top: targetElement.offsetTop - 80,
              behavior: 'smooth'
            });
            
            UIControls.closeNav();
          }
        });
      });
    },
  
    openNav() {
      document.getElementById('mySidebar').classList.add('open');
    },
  
    closeNav() {
      document.getElementById('mySidebar').classList.remove('open');
    }
  };
  
  // Initialize all functionality when DOM is loaded
  document.addEventListener('DOMContentLoaded', () => {
    LanguageManager.init();
    UIControls.init();
  });