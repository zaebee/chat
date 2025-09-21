/**
 * bee.Jules Guided Learning System
 * 
 * Provides interactive guidance and mentorship for Sacred Team challenges,
 * connecting students directly to real GitHub issues with AI-powered assistance.
 */

import { SacredChallenge, SacredMentor } from './challenges'

export interface JulesGuidanceSession {
  challengeId: string
  studentId: string
  startedAt: Date
  currentStep: number
  totalSteps: number
  guidanceHistory: JulesMessage[]
  issueUrl: string
  prUrl?: string
  status: 'active' | 'completed' | 'stuck' | 'abandoned'
}

export interface JulesMessage {
  id: string
  type: 'guidance' | 'hint' | 'encouragement' | 'correction' | 'celebration'
  message: string
  timestamp: Date
  codeExample?: string
  fileReference?: string
  issueReference?: number
}

export interface CodeReview {
  fileChanges: FileChange[]
  overallAssessment: 'excellent' | 'good' | 'needs_improvement' | 'requires_major_changes'
  sacredPrinciplesScore: {
    modularity: number
    legibility: number
    apiFirst: number
    observability: number
  }
  suggestions: string[]
  celebration?: string
}

export interface FileChange {
  filename: string
  changeType: 'added' | 'modified' | 'deleted'
  linesAdded: number
  linesRemoved: number
  assessment: 'excellent' | 'good' | 'needs_improvement'
  feedback: string
}

export class BeeJulesGuide {
  private activeSessions: Map<string, JulesGuidanceSession> = new Map()
  private guidanceTemplates: Map<string, JulesGuidanceTemplate> = new Map()

  constructor() {
    this.initializeGuidanceTemplates()
  }

  // Start guided learning session
  startGuidedChallenge(challengeId: string, studentId: string): JulesGuidanceSession {
    const challenge = this.getChallengeById(challengeId)
    if (!challenge) {
      throw new Error(`Challenge ${challengeId} not found`)
    }

    const session: JulesGuidanceSession = {
      challengeId,
      studentId,
      startedAt: new Date(),
      currentStep: 0,
      totalSteps: this.calculateTotalSteps(challenge),
      guidanceHistory: [],
      issueUrl: `https://github.com/zaebee/chat/issues/${challenge.issueNumber}`,
      status: 'active'
    }

    this.activeSessions.set(`${studentId}_${challengeId}`, session)

    // Send welcome message
    this.sendGuidanceMessage(session, 'guidance', this.getWelcomeMessage(challenge))

    return session
  }

  // Interactive guidance system
  requestNextStep(sessionKey: string): JulesMessage {
    const session = this.activeSessions.get(sessionKey)
    if (!session) {
      throw new Error('Session not found')
    }

    const challenge = this.getChallengeById(session.challengeId)!
    const template = this.guidanceTemplates.get(session.challengeId)!
    
    session.currentStep++
    
    if (session.currentStep <= template.steps.length) {
      const step = template.steps[session.currentStep - 1]
      return this.sendGuidanceMessage(session, 'guidance', step.instruction, step.codeExample, step.fileReference)
    } else {
      return this.sendGuidanceMessage(session, 'guidance', 'You\'ve completed all guided steps! Time to implement your solution and create a PR.')
    }
  }

  requestHint(sessionKey: string): JulesMessage {
    const session = this.activeSessions.get(sessionKey)
    if (!session) {
      throw new Error('Session not found')
    }

    const challenge = this.getChallengeById(session.challengeId)!
    const template = this.guidanceTemplates.get(session.challengeId)!
    
    const currentStepIndex = Math.max(0, session.currentStep - 1)
    const step = template.steps[currentStepIndex]
    
    if (step && step.hints.length > 0) {
      const hint = step.hints[Math.floor(Math.random() * step.hints.length)]
      return this.sendGuidanceMessage(session, 'hint', `💡 Hint: ${hint}`)
    } else {
      return this.sendGuidanceMessage(session, 'hint', '💡 You\'re on the right track! Trust your understanding of Sacred Team principles.')
    }
  }

  // Code review system
  reviewCode(sessionKey: string, fileChanges: FileChange[]): CodeReview {
    const session = this.activeSessions.get(sessionKey)
    if (!session) {
      throw new Error('Session not found')
    }

    const challenge = this.getChallengeById(session.challengeId)!
    
    // Analyze changes against Sacred Team principles
    const review: CodeReview = {
      fileChanges,
      overallAssessment: this.assessOverallQuality(fileChanges, challenge),
      sacredPrinciplesScore: this.scoreSacredPrinciples(fileChanges, challenge),
      suggestions: this.generateSuggestions(fileChanges, challenge)
    }

    // Add celebration if excellent
    if (review.overallAssessment === 'excellent') {
      review.celebration = this.generateCelebration(challenge)
      this.sendGuidanceMessage(session, 'celebration', review.celebration!)
    }

    return review
  }

  // PR creation guidance
  guidePRCreation(sessionKey: string): JulesMessage {
    const session = this.activeSessions.get(sessionKey)
    if (!session) {
      throw new Error('Session not found')
    }

    const challenge = this.getChallengeById(session.challengeId)!
    
    const prGuidance = `
🎯 **Time to create your Sacred Team PR!**

Follow these steps:

1. **Create a branch**: \`git checkout -b fix/issue-${challenge.issueNumber}-${challenge.title.toLowerCase().replace(/[^a-z0-9]/g, '-')}\`

2. **Commit your changes**: 
   \`\`\`bash
   git add .
   git commit -m "${this.generateCommitMessage(challenge)}"
   \`\`\`

3. **Push and create PR**:
   \`\`\`bash
   git push -u origin your-branch-name
   gh pr create --title "${challenge.title}" --body "Closes #${challenge.issueNumber}"
   \`\`\`

4. **Request Sacred Team review** by mentioning the issue in your PR description.

Remember: Your PR will be reviewed by the Sacred Team using our bee-to-peer cross review protocol! 🏛️
    `

    return this.sendGuidanceMessage(session, 'guidance', prGuidance)
  }

  // Helper methods
  private sendGuidanceMessage(
    session: JulesGuidanceSession, 
    type: JulesMessage['type'], 
    message: string,
    codeExample?: string,
    fileReference?: string
  ): JulesMessage {
    const julesMessage: JulesMessage = {
      id: `jules_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type,
      message,
      timestamp: new Date(),
      codeExample,
      fileReference
    }

    session.guidanceHistory.push(julesMessage)
    return julesMessage
  }

  private getChallengeById(challengeId: string): SacredChallenge | undefined {
    // This would import from challenges.ts in real implementation
    // For now, return a mock challenge
    return {
      id: challengeId,
      issueNumber: 15,
      title: 'Add Explanations for Numerical Constants',
      description: 'Learn sacred legibility',
      difficulty: 'bee.larva',
      mentor: 'bee.jules',
      atcgClassification: 'T',
      sacredPrinciples: ['Legibility'],
      learningObjectives: ['Document code clearly'],
      divineRewards: { xp: 100, sacredInsights: [] },
      estimatedTime: '30 minutes',
      files: ['frontend/src/utils/emotionalContagion.ts'],
      mentorGuidance: {
        introduction: 'Welcome to your first challenge!',
        hints: ['Look for magic numbers'],
        sacredWisdom: 'Clear code tells a story'
      },
      successCriteria: ['All constants documented'],
      tags: ['documentation']
    }
  }

  private calculateTotalSteps(challenge: SacredChallenge): number {
    const template = this.guidanceTemplates.get(challenge.id)
    return template ? template.steps.length : 5
  }

  private getWelcomeMessage(challenge: SacredChallenge): string {
    return `
🔧 **Welcome to bee.Jules Guided Learning!**

I'm here to guide you through **${challenge.title}** step by step.

**Challenge Overview:**
- 🎯 **Difficulty**: ${challenge.difficulty}
- 🧬 **ATCG Classification**: ${challenge.atcgClassification}
- 🏛️ **Sacred Principles**: ${challenge.sacredPrinciples.join(', ')}
- ⏱️ **Estimated Time**: ${challenge.estimatedTime}

**What you'll learn:**
${challenge.learningObjectives.map(obj => `• ${obj}`).join('\n')}

**GitHub Issue**: [#${challenge.issueNumber}](https://github.com/zaebee/chat/issues/${challenge.issueNumber})

Ready to begin? Request the next step when you're prepared to start coding! 🚀
    `
  }

  private assessOverallQuality(fileChanges: FileChange[], challenge: SacredChallenge): CodeReview['overallAssessment'] {
    const scores = fileChanges.map(change => {
      switch (change.assessment) {
        case 'excellent': return 4
        case 'good': return 3
        case 'needs_improvement': return 2
        default: return 1
      }
    })

    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length

    if (avgScore >= 3.5) return 'excellent'
    if (avgScore >= 2.5) return 'good'
    if (avgScore >= 1.5) return 'needs_improvement'
    return 'requires_major_changes'
  }

  private scoreSacredPrinciples(fileChanges: FileChange[], challenge: SacredChallenge) {
    // Mock scoring - in real implementation, this would analyze the actual code
    return {
      modularity: 0.85,
      legibility: 0.90,
      apiFirst: 0.80,
      observability: 0.75
    }
  }

  private generateSuggestions(fileChanges: FileChange[], challenge: SacredChallenge): string[] {
    const suggestions = [
      'Consider adding more descriptive comments explaining the "why" behind your changes',
      'Ensure your variable names clearly express their purpose',
      'Check that your solution follows the Sacred Team principles'
    ]

    // Add challenge-specific suggestions
    if (challenge.sacredPrinciples.includes('Modularity')) {
      suggestions.push('Verify that each function has a single, clear responsibility')
    }

    return suggestions
  }

  private generateCelebration(challenge: SacredChallenge): string {
    const celebrations = [
      `🎉 Excellent work! Your solution perfectly embodies the Sacred Team principles of ${challenge.sacredPrinciples.join(' and ')}.`,
      `✨ Outstanding! You've demonstrated mastery of ${challenge.atcgClassification} transformation patterns.`,
      `🏛️ Magnificent! Your code quality would make the entire Sacred Team proud.`
    ]

    return celebrations[Math.floor(Math.random() * celebrations.length)]
  }

  private generateCommitMessage(challenge: SacredChallenge): string {
    return `${challenge.title.toLowerCase()}

Resolves #${challenge.issueNumber}

Co-authored-by: bee.Jules <bee.jules@sacred.team>`
  }

  private initializeGuidanceTemplates(): void {
    // Template for constants explanation challenge
    this.guidanceTemplates.set('larva_constants_explanation', {
      challengeId: 'larva_constants_explanation',
      steps: [
        {
          instruction: `
📖 **Step 1: Identify the Magic Numbers**

Open \`frontend/src/utils/emotionalContagion.ts\` and look for numerical constants that lack explanation.

Look for lines like:
- \`EMOTIONAL_HISTORY_LENGTH = 10\`
- \`RECENT_HISTORY_SAMPLE = 5\`

These numbers tell us "what" but not "why". Your sacred mission is to explain the reasoning behind each value.
          `,
          hints: [
            'Search for variables with numeric values',
            'Ask yourself: why this specific number?',
            'Consider the impact if the number was different'
          ],
          fileReference: 'frontend/src/utils/emotionalContagion.ts'
        },
        {
          instruction: `
✍️ **Step 2: Add Sacred Documentation**

For each constant, add a comment explaining:
1. **Why** this specific value was chosen
2. **What happens** if it's too high or too low
3. **How it affects** the system behavior

Example:
\`\`\`typescript
// Keep last 10 emotional states for trend analysis
// Too few (< 5) = insufficient data for patterns
// Too many (> 20) = outdated emotions affecting current state
const EMOTIONAL_HISTORY_LENGTH = 10
\`\`\`
          `,
          codeExample: `
// Keep last 10 emotional states for trend analysis
// Too few (< 5) = insufficient data for patterns  
// Too many (> 20) = outdated emotions affecting current state
const EMOTIONAL_HISTORY_LENGTH = 10

// Sample 5 recent states for current mood calculation
// Balances responsiveness with stability
const RECENT_HISTORY_SAMPLE = 5
          `,
          hints: [
            'Explain the reasoning, not just what the code does',
            'Consider edge cases (too high/too low values)',
            'Think about the user experience impact'
          ],
          fileReference: 'frontend/src/utils/emotionalContagion.ts'
        },
        {
          instruction: `
🔍 **Step 3: Review Your Documentation**

Check that your comments:
- ✅ Explain the "why" behind each value
- ✅ Are clear to someone unfamiliar with the code
- ✅ Help future teammates understand the reasoning
- ✅ Follow Sacred Team legibility principles

Remember: Sacred Team code should tell a story that any teammate can understand! 📜
          `,
          hints: [
            'Read your comments as if you\'re seeing the code for the first time',
            'Ask: would a new team member understand why these values were chosen?',
            'Ensure comments add value beyond what the code already shows'
          ]
        }
      ]
    })

    // Add more templates for other challenges...
  }
}

interface JulesGuidanceTemplate {
  challengeId: string
  steps: GuidanceStep[]
}

interface GuidanceStep {
  instruction: string
  hints: string[]
  codeExample?: string
  fileReference?: string
}

// Export singleton instance
export const beeJulesGuide = new BeeJulesGuide()