#!/usr/bin/env node
/**
 * Frontend Purification Test
 * Validates pure frontend components for ontological purity and functionality
 */

const fs = require('fs');
const path = require('path');

class FrontendPurificationValidator {
  constructor() {
    this.violations = [];
    this.warnings = [];
    this.testResults = [];
  }

  async validateAll() {
    console.log('🔍 Frontend Purification Validation');
    console.log('=' .repeat(50));
    
    this.validateOntologicalPurity();
    this.validateFileStructure();
    this.validateNamingConsistency();
    this.validateTranslationLayer();
    
    this.printResults();
    return this.violations.length === 0;
  }

  validateOntologicalPurity() {
    console.log('\n🔮 Testing Ontological Purity...');
    
    const forbiddenTerms = [
      'sacred', 'divine', 'holy', 'blessed', 'mystical',
      'ionic', 'covalent', 'chemical', 'bond', 'lattice',
      'quantum', 'cosmic', 'celestial', 'transcendent'
    ];
    
    const filesToCheck = [
      'frontend/src/assets/js/components/aggregate/DataAggregator.ts',
      'frontend/src/assets/js/components/transformation/DataTransformer.ts',
      'frontend/src/translation/TranslationLayer.ts'
    ];
    
    let violationsFound = false;
    
    filesToCheck.forEach(filePath => {
      if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf8');
        const lines = content.split('\n');
        
        lines.forEach((line, index) => {
          // Skip comments
          if (line.trim().startsWith('//') || line.trim().startsWith('*')) {
            return;
          }
          
          forbiddenTerms.forEach(term => {
            if (line.toLowerCase().includes(term.toLowerCase())) {
              this.violations.push(
                `Ontological violation in ${filePath}:${index + 1} - ` +
                `forbidden term '${term}' found`
              );
              violationsFound = true;
            }
          });
        });
      } else {
        this.violations.push(`Missing file: ${filePath}`);
        violationsFound = true;
      }
    });
    
    if (!violationsFound) {
      console.log('   ✅ No ontological violations found');
      this.recordTest('Ontological Purity', true, 'No forbidden terms detected');
    } else {
      console.log('   ❌ Ontological violations detected');
      this.recordTest('Ontological Purity', false, 'Forbidden terms found');
    }
  }

  validateFileStructure() {
    console.log('\n📁 Testing File Structure...');
    
    const expectedFiles = [
      'frontend/src/assets/js/components/aggregate/DataAggregator.ts',
      'frontend/src/assets/js/components/transformation/DataTransformer.ts',
      'frontend/src/translation/TranslationLayer.ts'
    ];
    
    const backupFiles = [
      'frontend/src/assets/js/components/aggregate/SacredAggregator.ts.backup',
      'frontend/src/assets/js/components/transformation/SacredLambdaEngine.ts.backup'
    ];
    
    let structureValid = true;
    
    // Check expected files exist
    expectedFiles.forEach(filePath => {
      if (!fs.existsSync(filePath)) {
        this.violations.push(`Missing expected file: ${filePath}`);
        structureValid = false;
      }
    });
    
    // Check backup files exist
    backupFiles.forEach(filePath => {
      if (!fs.existsSync(filePath)) {
        this.warnings.push(`Missing backup file: ${filePath}`);
      }
    });
    
    if (structureValid) {
      console.log('   ✅ File structure is correct');
      this.recordTest('File Structure', true, 'All expected files present');
    } else {
      console.log('   ❌ File structure issues detected');
      this.recordTest('File Structure', false, 'Missing expected files');
    }
  }

  validateNamingConsistency() {
    console.log('\n📝 Testing Naming Consistency...');
    
    const namingTests = [
      {
        file: 'frontend/src/assets/js/components/aggregate/DataAggregator.ts',
        expectedClass: 'DataAggregator',
        expectedInterface: 'DataItem'
      },
      {
        file: 'frontend/src/assets/js/components/transformation/DataTransformer.ts',
        expectedClass: 'DataTransformer',
        expectedInterface: 'DataVector'
      }
    ];
    
    let namingValid = true;
    
    namingTests.forEach(test => {
      if (fs.existsSync(test.file)) {
        const content = fs.readFileSync(test.file, 'utf8');
        
        if (!content.includes(`class ${test.expectedClass}`)) {
          this.violations.push(
            `Missing expected class ${test.expectedClass} in ${test.file}`
          );
          namingValid = false;
        }
        
        if (!content.includes(`interface ${test.expectedInterface}`)) {
          this.violations.push(
            `Missing expected interface ${test.expectedInterface} in ${test.file}`
          );
          namingValid = false;
        }
      }
    });
    
    if (namingValid) {
      console.log('   ✅ Naming consistency validated');
      this.recordTest('Naming Consistency', true, 'All expected names found');
    } else {
      console.log('   ❌ Naming consistency issues detected');
      this.recordTest('Naming Consistency', false, 'Missing expected names');
    }
  }

  validateTranslationLayer() {
    console.log('\n🔄 Testing Translation Layer Updates...');
    
    const translationFile = 'frontend/src/translation/TranslationLayer.ts';
    
    if (!fs.existsSync(translationFile)) {
      this.violations.push(`Missing translation layer file: ${translationFile}`);
      this.recordTest('Translation Layer', false, 'File missing');
      return;
    }
    
    const content = fs.readFileSync(translationFile, 'utf8');
    
    const expectedMappings = [
      'DataAggregator',
      'DataTransformer',
      'DataConnector',
      'DataGenerator'
    ];
    
    let translationValid = true;
    
    expectedMappings.forEach(mapping => {
      if (!content.includes(mapping)) {
        this.violations.push(
          `Missing expected mapping '${mapping}' in translation layer`
        );
        translationValid = false;
      }
    });
    
    // Check for legacy support
    const legacyMappings = [
      'SacredAggregator',
      'SacredLambdaEngine'
    ];
    
    legacyMappings.forEach(mapping => {
      if (!content.includes(mapping)) {
        this.warnings.push(
          `Missing legacy mapping '${mapping}' in translation layer`
        );
      }
    });
    
    if (translationValid) {
      console.log('   ✅ Translation layer updated correctly');
      this.recordTest('Translation Layer', true, 'All mappings present');
    } else {
      console.log('   ❌ Translation layer issues detected');
      this.recordTest('Translation Layer', false, 'Missing mappings');
    }
  }

  recordTest(testName, passed, details) {
    this.testResults.push({
      test: testName,
      passed,
      details,
      timestamp: new Date().toISOString()
    });
  }

  printResults() {
    console.log('\n' + '='.repeat(50));
    console.log('📊 FRONTEND PURIFICATION RESULTS');
    console.log('='.repeat(50));
    
    const totalTests = this.testResults.length;
    const passedTests = this.testResults.filter(r => r.passed).length;
    const failedTests = totalTests - passedTests;
    const successRate = totalTests > 0 ? (passedTests / totalTests * 100) : 0;
    
    console.log(`📈 Test Summary:`);
    console.log(`   Total Tests: ${totalTests}`);
    console.log(`   Passed: ${passedTests}`);
    console.log(`   Failed: ${failedTests}`);
    console.log(`   Success Rate: ${successRate.toFixed(1)}%`);
    console.log();
    
    if (this.violations.length > 0) {
      console.log(`❌ VIOLATIONS (${this.violations.length}):`);
      this.violations.forEach(violation => {
        console.log(`   • ${violation}`);
      });
      console.log();
    }
    
    if (this.warnings.length > 0) {
      console.log(`⚠️  WARNINGS (${this.warnings.length}):`);
      this.warnings.forEach(warning => {
        console.log(`   • ${warning}`);
      });
      console.log();
    }
    
    console.log(`📋 Detailed Results:`);
    this.testResults.forEach(result => {
      const status = result.passed ? '✅ PASS' : '❌ FAIL';
      console.log(`   ${result.test}: ${status} - ${result.details}`);
    });
    console.log();
    
    if (this.violations.length === 0) {
      console.log('🎉 FRONTEND PURIFICATION SUCCESSFUL!');
      console.log('✅ All components are ontologically pure');
      console.log('🔧 Ready for protobuf integration');
    } else {
      console.log('❌ FRONTEND PURIFICATION FAILED!');
      console.log('💀 Fix violations before proceeding');
    }
    
    console.log();
    console.log('📋 Ready for bee-to-peer review');
    console.log('='.repeat(50));
  }
}

async function main() {
  const validator = new FrontendPurificationValidator();
  const success = await validator.validateAll();
  process.exit(success ? 0 : 1);
}

if (require.main === module) {
  main().catch(console.error);
}