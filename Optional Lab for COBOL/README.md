# Optional Lab for COBOL - Legacy Modernization with IBM Bob

## Overview

This optional lab demonstrates how to use **IBM Bob** to modernize legacy COBOL financial applications into modern Java microservices. Using real IBM sample programs from the Debug for z/OS documentation, you'll learn how AI can accelerate mainframe modernization projects.

## What's Included

This lab contains:
- **Three COBOL Programs**: A financial calculator system from IBM's mainframe samples
  - `COBCALC.cbl` - Main controller program
  - `COBLOAN.cbl` - Loan payment calculator subprogram  
  - `COBVALU.cbl` - Present value calculator subprogram
- **Workshop Guide**: `WORKSHOP-COBOL2JAVA.md` - Complete step-by-step modernization workshop

## Workshop Objectives

Learn how IBM Bob can:
- ✅ Analyze and understand legacy COBOL code patterns
- ✅ Convert COBOL to modern Java with proper design patterns
- ✅ Generate comprehensive test suites for validation
- ✅ Build modern user interfaces for legacy business logic
- ✅ Create REST APIs for microservice integration
- ✅ Support safe, incremental modernization strategies

## Target Audience

- Enterprise software engineers
- Mainframe developers
- Modernization architects
- Anyone working with legacy COBOL systems and Java migration projects

## Time Required

**30-45 minutes** for the complete workshop

## Prerequisites

### Required Software
- Java 11 or higher (OpenJDK 21 recommended)
- Apache Maven 3.6+
- IDE (VS Code, IntelliJ, or Eclipse)
- IBM Bob AI Assistant

### Setup Instructions

Detailed setup instructions for macOS, Windows, and Linux are provided in the workshop guide.

**Quick Start (macOS)**:
```bash
# Install Java and Maven
brew install openjdk@21 maven

# Set JAVA_HOME
export JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home

# Verify installation
java -version
mvn -version
```

## Getting Started

1. **Read the Workshop Guide**: Open [`WORKSHOP-COBOL2JAVA.md`](WORKSHOP-COBOL2JAVA.md) for complete instructions
2. **Review the COBOL Code**: Examine the three `.cbl` files to understand the legacy system
3. **Follow the Steps**: Work through the 7-step modernization process with IBM Bob
4. **Build and Test**: Create a modern Java application from the legacy COBOL code

## Workshop Steps

The workshop guides you through:

1. **Understand the COBOL Code** (5 min) - Deep analysis of legacy patterns
2. **Convert to Java** (10 min) - Modern object-oriented design
3. **Create Comprehensive Tests** (8 min) - JUnit test suite with edge cases
4. **Build Interactive UI** (10 min) - JavaFX/Swing interface
5. **Add REST API** (7 min) - Microservice wrapper
6. **Performance Comparison** (5 min, optional) - Benchmark results
7. **Documentation Generation** (5 min, optional) - API docs and diagrams

## What You'll Build

By the end of this workshop, you'll have:
- ✅ Modern Java implementation of COBOL financial calculators
- ✅ Comprehensive test suite (19+ tests)
- ✅ Interactive GUI application
- ✅ REST API microservice
- ✅ Complete documentation

## Key Learning Outcomes

### Technical Skills
- COBOL to Java conversion patterns
- Financial calculation precision (BigDecimal)
- Test-driven migration strategies
- Modern UI development
- REST API design

### Modernization Patterns
- Data type mapping (COBOL COMP → Java BigDecimal)
- Subprogram conversion (CALL/LINKAGE → Methods/Objects)
- Legacy pattern recognition (REDEFINES, UNSTRING, INSPECT)
- Financial calculation preservation
- Error handling modernization

## Real-World Applications

These patterns apply to:
- Banking and financial services modernization
- Insurance policy calculation systems
- Payroll and benefits processing
- Inventory and pricing systems
- Any COBOL system with complex business logic

## Source Attribution

The COBOL programs in this lab are IBM sample programs from the Debug for z/OS documentation:
- **Source**: IBM Debug for z/OS Sample Programs
- **Reference**: https://www.ibm.com/docs/en/debug-for-zos/16.0.x?topic=mode-example-sample-cobol-program-debugging

## Support

For questions or issues with this lab:
- Review the detailed workshop guide
- Check the Prerequisites section for setup requirements
- Ensure Java and Maven are properly configured

## Next Steps

After completing this lab:
- Apply these patterns to your own COBOL codebases
- Extend with additional features (reporting, audit trails)
- Integrate with modern data stores (PostgreSQL, MongoDB)
- Deploy to cloud platforms (AWS, Azure, IBM Cloud)
- Implement CI/CD pipelines for continuous modernization

---

**Lab Version**: 1.0  
**Difficulty Level**: Intermediate  
**Estimated Time**: 30-45 minutes