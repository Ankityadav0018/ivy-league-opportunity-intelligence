/**
 * Cursor Shining Effect
 * Creates a magical sparkle trail that follows the cursor
 */

class CursorEffect {
    constructor() {
        this.particles = [];
        this.cursorX = 0;
        this.cursorY = 0;
        this.isMoving = false;
        this.canvas = null;
        this.ctx = null;
        
        this.init();
    }
    
    init() {
        // Create canvas for particles
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'cursor-canvas';
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '9999';
        document.body.appendChild(this.canvas);
        
        this.ctx = this.canvas.getContext('2d');
        this.resizeCanvas();
        
        // Create cursor glow element
        this.createCursorGlow();
        
        // Event listeners
        window.addEventListener('resize', () => this.resizeCanvas());
        document.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        document.addEventListener('mouseenter', () => this.isMoving = true);
        document.addEventListener('mouseleave', () => this.isMoving = false);
        
        // Start animation loop
        this.animate();
    }
    
    createCursorGlow() {
        const glow = document.createElement('div');
        glow.id = 'cursor-glow';
        glow.style.cssText = `
            position: fixed;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            pointer-events: none;
            z-index: 9998;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.8), rgba(236, 72, 153, 0.4), transparent);
            transform: translate(-50%, -50%);
            transition: opacity 0.3s ease;
            opacity: 0;
        `;
        document.body.appendChild(glow);
        this.cursorGlow = glow;
    }
    
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    handleMouseMove(e) {
        this.cursorX = e.clientX;
        this.cursorY = e.clientY;
        this.isMoving = true;
        
        // Update cursor glow position
        this.cursorGlow.style.left = this.cursorX + 'px';
        this.cursorGlow.style.top = this.cursorY + 'px';
        this.cursorGlow.style.opacity = '1';
        
        // Create particles
        if (Math.random() > 0.3) { // 70% chance to create particle
            this.createParticle(this.cursorX, this.cursorY);
        }
    }
    
    createParticle(x, y) {
        const particle = {
            x: x + (Math.random() - 0.5) * 10,
            y: y + (Math.random() - 0.5) * 10,
            size: Math.random() * 4 + 2,
            speedX: (Math.random() - 0.5) * 2,
            speedY: (Math.random() - 0.5) * 2,
            life: 1,
            decay: Math.random() * 0.02 + 0.01,
            color: this.getRandomColor(),
            rotation: Math.random() * Math.PI * 2,
            rotationSpeed: (Math.random() - 0.5) * 0.2
        };
        
        this.particles.push(particle);
        
        // Limit particles for performance
        if (this.particles.length > 100) {
            this.particles.shift();
        }
    }
    
    getRandomColor() {
        const colors = [
            'rgba(99, 102, 241, ', // Primary
            'rgba(236, 72, 153, ', // Secondary
            'rgba(20, 184, 166, ', // Accent
            'rgba(255, 255, 255, ', // White
            'rgba(251, 191, 36, '  // Gold
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }
    
    updateParticles() {
        this.particles = this.particles.filter(particle => {
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            particle.life -= particle.decay;
            particle.rotation += particle.rotationSpeed;
            particle.speedY += 0.05; // Slight gravity
            
            return particle.life > 0;
        });
    }
    
    drawParticles() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(particle => {
            this.ctx.save();
            
            // Translate to particle position
            this.ctx.translate(particle.x, particle.y);
            this.ctx.rotate(particle.rotation);
            
            // Draw star/sparkle shape
            this.ctx.globalAlpha = particle.life;
            
            // Draw glow effect
            const gradient = this.ctx.createRadialGradient(0, 0, 0, 0, 0, particle.size * 2);
            gradient.addColorStop(0, particle.color + particle.life + ')');
            gradient.addColorStop(0.5, particle.color + (particle.life * 0.5) + ')');
            gradient.addColorStop(1, particle.color + '0)');
            
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(0, 0, particle.size * 2, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Draw star shape
            this.ctx.fillStyle = particle.color + particle.life + ')';
            this.ctx.beginPath();
            
            for (let i = 0; i < 5; i++) {
                const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
                const x = Math.cos(angle) * particle.size;
                const y = Math.sin(angle) * particle.size;
                
                if (i === 0) {
                    this.ctx.moveTo(x, y);
                } else {
                    this.ctx.lineTo(x, y);
                }
                
                const innerAngle = angle + Math.PI / 5;
                const innerX = Math.cos(innerAngle) * (particle.size * 0.5);
                const innerY = Math.sin(innerAngle) * (particle.size * 0.5);
                this.ctx.lineTo(innerX, innerY);
            }
            
            this.ctx.closePath();
            this.ctx.fill();
            
            this.ctx.restore();
        });
    }
    
    animate() {
        this.updateParticles();
        this.drawParticles();
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize cursor effect when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on devices with a mouse (not touch devices)
    if (window.matchMedia('(pointer: fine)').matches) {
        new CursorEffect();
    }
});
