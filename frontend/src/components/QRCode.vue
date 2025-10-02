<template>
  <div class="qr-code-container">
    <div class="qr-code-wrapper" :class="{ 'large': size === 'large', 'small': size === 'small' }">
      <div class="qr-code-header" v-if="title">
        <h3>{{ title }}</h3>
        <p v-if="subtitle">{{ subtitle }}</p>
      </div>
      
      <div class="qr-code-display">
        <div class="qr-pattern">
          <!-- QR Code Pattern Simulation -->
          <div class="qr-grid">
            <div v-for="(row, rowIndex) in qrPattern" :key="rowIndex" class="qr-row">
              <div 
                v-for="(cell, cellIndex) in row" 
                :key="cellIndex" 
                :class="['qr-cell', { 'filled': cell }]"
              ></div>
            </div>
          </div>
          
          <!-- Corner markers -->
          <div class="corner-marker top-left"></div>
          <div class="corner-marker top-right"></div>
          <div class="corner-marker bottom-left"></div>
        </div>
      </div>
      
      <div class="qr-code-info" v-if="showCode">
        <div class="code-display">
          <span class="code-label">Code:</span>
          <span class="code-value">{{ code }}</span>
          <button 
            class="copy-btn" 
            @click="copyCode"
            :class="{ 'copied': isCopied }"
          >
            {{ isCopied ? '✓' : '📋' }}
          </button>
        </div>
      </div>
      
      <div class="qr-instructions" v-if="instructions">
        <p>{{ instructions }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QRCode',
  props: {
    code: {
      type: String,
      required: true
    },
    title: {
      type: String,
      default: ''
    },
    subtitle: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'medium', // small, medium, large
      validator: value => ['small', 'medium', 'large'].includes(value)
    },
    showCode: {
      type: Boolean,
      default: true
    },
    instructions: {
      type: String,
      default: ''
    },
    theme: {
      type: String,
      default: 'light', // light, dark
      validator: value => ['light', 'dark'].includes(value)
    }
  },
  data() {
    return {
      isCopied: false,
      qrPattern: []
    }
  },
  mounted() {
    this.generateQRPattern();
  },
  watch: {
    code() {
      this.generateQRPattern();
    }
  },
  methods: {
    generateQRPattern() {
      // Generate a pseudo-random QR code pattern based on the code
      const size = 21; // Standard QR code size
      const pattern = [];
      
      // Create a seed from the code
      let seed = 0;
      for (let i = 0; i < this.code.length; i++) {
        seed += this.code.charCodeAt(i);
      }
      
      // Simple pseudo-random number generator
      const random = (seed) => {
        const x = Math.sin(seed) * 10000;
        return x - Math.floor(x);
      };
      
      for (let row = 0; row < size; row++) {
        const rowPattern = [];
        for (let col = 0; col < size; col++) {
          // Skip corner markers and timing patterns
          if (this.isCornerMarker(row, col, size) || this.isTimingPattern(row, col)) {
            rowPattern.push(false);
          } else {
            // Generate pseudo-random pattern
            const cellSeed = seed + row * size + col;
            rowPattern.push(random(cellSeed) > 0.5);
          }
        }
        pattern.push(rowPattern);
      }
      
      this.qrPattern = pattern;
    },
    
    isCornerMarker(row, col, size) {
      // Top-left corner
      if (row < 7 && col < 7) return true;
      // Top-right corner
      if (row < 7 && col >= size - 7) return true;
      // Bottom-left corner
      if (row >= size - 7 && col < 7) return true;
      return false;
    },
    
    isTimingPattern(row, col) {
      // Horizontal timing pattern
      if (row === 6) return true;
      // Vertical timing pattern
      if (col === 6) return true;
      return false;
    },
    
    async copyCode() {
      try {
        await navigator.clipboard.writeText(this.code);
        this.isCopied = true;
        setTimeout(() => {
          this.isCopied = false;
        }, 2000);
      } catch (err) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = this.code;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        this.isCopied = true;
        setTimeout(() => {
          this.isCopied = false;
        }, 2000);
      }
    }
  }
}
</script>

<style scoped>
.qr-code-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.qr-code-wrapper {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 300px;
  width: 100%;
  border: 3px solid #f0f0f0;
  transition: all 0.3s ease;
}

.qr-code-wrapper:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.qr-code-wrapper.large {
  max-width: 400px;
  padding: 40px;
}

.qr-code-wrapper.small {
  max-width: 200px;
  padding: 20px;
}

.qr-code-header h3 {
  font-size: 1.4rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 8px 0;
  background: linear-gradient(135deg, #ff4757, #ff3742);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.qr-code-header p {
  font-size: 0.9rem;
  color: #666;
  margin: 0 0 20px 0;
}

.qr-code-display {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
}

.qr-pattern {
  position: relative;
  background: white;
  border: 2px solid #e1e1e1;
  border-radius: 12px;
  padding: 15px;
  display: inline-block;
}

.qr-grid {
  display: grid;
  grid-template-columns: repeat(21, 1fr);
  gap: 1px;
  width: 168px;
  height: 168px;
}

.qr-code-wrapper.large .qr-grid {
  width: 210px;
  height: 210px;
}

.qr-code-wrapper.small .qr-grid {
  width: 126px;
  height: 126px;
}

.qr-row {
  display: contents;
}

.qr-cell {
  width: 100%;
  height: 100%;
  background: white;
  transition: all 0.1s ease;
}

.qr-cell.filled {
  background: #333;
}

/* Corner markers */
.corner-marker {
  position: absolute;
  width: 42px;
  height: 42px;
  border: 3px solid #333;
  background: white;
}

.corner-marker::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 18px;
  height: 18px;
  background: #333;
  border-radius: 2px;
}

.corner-marker.top-left {
  top: 15px;
  left: 15px;
}

.corner-marker.top-right {
  top: 15px;
  right: 15px;
}

.corner-marker.bottom-left {
  bottom: 15px;
  left: 15px;
}

.qr-code-info {
  margin-top: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.code-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.code-label {
  font-weight: 600;
  color: #666;
  font-size: 0.9rem;
}

.code-value {
  font-family: 'Courier New', monospace;
  font-weight: 700;
  color: #333;
  font-size: 1.1rem;
  background: white;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ddd;
  letter-spacing: 1px;
}

.copy-btn {
  background: #ff4757;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
  min-width: 40px;
}

.copy-btn:hover {
  background: #ff3742;
  transform: scale(1.05);
}

.copy-btn.copied {
  background: #00b894;
  transform: scale(1.1);
}

.qr-instructions {
  margin-top: 15px;
  padding: 12px;
  background: linear-gradient(135deg, #ff4757, #ff3742);
  color: white;
  border-radius: 8px;
  font-size: 0.9rem;
  line-height: 1.4;
}

.qr-instructions p {
  margin: 0;
  font-weight: 500;
}

/* Dark theme support */
.dark-mode .qr-code-wrapper {
  background: #2d2d2d;
  border-color: #4a4a4a;
}

.dark-mode .qr-code-header h3 {
  color: #f5f5f5;
}

.dark-mode .qr-code-header p {
  color: #b8b8b8;
}

.dark-mode .qr-pattern {
  background: #3a3a3a;
  border-color: #4a4a4a;
}

.dark-mode .qr-cell {
  background: #3a3a3a;
}

.dark-mode .qr-cell.filled {
  background: #f5f5f5;
}

.dark-mode .corner-marker {
  border-color: #f5f5f5;
  background: #3a3a3a;
}

.dark-mode .corner-marker::after {
  background: #f5f5f5;
}

.dark-mode .qr-code-info {
  background: #3a3a3a;
  border-color: #4a4a4a;
}

.dark-mode .code-label {
  color: #b8b8b8;
}

.dark-mode .code-value {
  background: #4a4a4a;
  color: #f5f5f5;
  border-color: #5a5a5a;
}

/* Responsive design */
@media (max-width: 480px) {
  .qr-code-container {
    padding: 15px;
  }
  
  .qr-code-wrapper {
    padding: 20px;
    max-width: 280px;
  }
  
  .qr-grid {
    width: 140px;
    height: 140px;
  }
  
  .corner-marker {
    width: 35px;
    height: 35px;
  }
  
  .corner-marker::after {
    width: 15px;
    height: 15px;
  }
  
  .code-display {
    flex-direction: column;
    gap: 8px;
  }
  
  .code-value {
    font-size: 1rem;
    padding: 6px 10px;
  }
}

/* Animation for QR code generation */
@keyframes qrGenerate {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.qr-pattern {
  animation: qrGenerate 0.5s ease-out;
}

/* Pulse animation for copy success */
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.copy-btn.copied {
  animation: pulse 0.3s ease-in-out;
}
</style>
