# IBM Bob Workshop - Legacy COBOL Modernization to Java
## Case Study: Financial Calculator (COBOL to Java Migration)

### Audience
Enterprise software engineers, mainframe developers, and modernization architects working with legacy COBOL systems and Java migration projects.

### Goal of the Workshop
Demonstrate how **IBM Bob** can:
- Understand legacy COBOL financial applications
- Analyze non-obvious COBOL patterns and idioms
- Generate modern Java equivalents with proper design patterns
- Create comprehensive test suites for validation
- Build modern user interfaces for legacy business logic
- Support safe, incremental modernization strategies

We use a **COBOL Financial Calculator** consisting of three programs (COBCALC, COBLOAN, COBVALU) as a realistic example of mainframe financial software.

**Source**: IBM Debug for z/OS Sample Programs
**Reference**: https://www.ibm.com/docs/en/debug-for-zos/16.0.x?topic=mode-example-sample-cobol-program-debugging

---

## Workshop Flow Overview

1. **Understand the COBOL code** - Deep analysis of legacy patterns
2. **Convert to Java** - Modern object-oriented design
3. **Create comprehensive tests** - JUnit test suite with edge cases
4. **Build interactive UI** - JavaFX/Swing interface for user input
5. **Add REST API** - Microservice wrapper for the calculators
6. **Performance comparison** - Benchmark COBOL vs Java implementations
7. **Documentation generation** - API docs and architecture diagrams

Each step builds on the previous one and mirrors real-world modernization projects.

**Estimated Time:** 30-45 minutes

---

## Prerequisites

### System Requirements
- macOS, Linux, or Windows
- Terminal/Command Line access
- Text editor or IDE (VS Code recommended)
- Internet connection for downloading dependencies

### Pre-Workshop Setup (macOS)

**Important**: Complete these steps before starting the workshop to ensure Java and Maven are properly configured.

#### 1. Install OpenJDK 21
```bash
# Install OpenJDK 21 (JDK, not just JRE) via Homebrew
brew install openjdk@21
```

#### 2. Install Apache Maven
```bash
# Install Maven via Homebrew (may also pull in openjdk 25 as a dependency)
brew install maven
```

#### 3. Set JAVA_HOME Environment Variable
```bash
# Set JAVA_HOME to the JDK 21 installation
# This is needed before running any mvn or java commands
export JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home
```

**Note**: To make JAVA_HOME permanent, add the export command to your shell profile:
```bash
# For bash users
echo 'export JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home' >> ~/.bash_profile
source ~/.bash_profile

# For zsh users (default on modern macOS)
echo 'export JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home' >> ~/.zshrc
source ~/.zshrc
```

#### 4. Verify Installation
```bash
# Check Java version (should show OpenJDK 21)
java -version

# Check Maven version (should show Maven 3.6+)
mvn -version

# Verify JAVA_HOME is set correctly
echo $JAVA_HOME
```

Expected output:
```
openjdk version "21.x.x" ...
Apache Maven 3.x.x ...
/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home
```

### Pre-Workshop Setup (Windows)

#### 1. Install OpenJDK 21
- Download from: https://adoptium.net/temurin/releases/?version=21
- Run the installer and select "Add to PATH" option

#### 2. Install Apache Maven
- Download from: https://maven.apache.org/download.cgi
- Extract to `C:\Program Files\Maven`
- Add `C:\Program Files\Maven\bin` to PATH

#### 3. Set JAVA_HOME
- Open System Properties → Environment Variables
- Add new system variable: `JAVA_HOME` = `C:\Program Files\Eclipse Adoptium\jdk-21.x.x`
- Verify in Command Prompt: `echo %JAVA_HOME%`

### Pre-Workshop Setup (Linux)

#### 1. Install OpenJDK 21
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-21-jdk

# Fedora/RHEL
sudo dnf install java-21-openjdk-devel
```

#### 2. Install Maven
```bash
# Ubuntu/Debian
sudo apt install maven

# Fedora/RHEL
sudo dnf install maven
```

#### 3. Set JAVA_HOME
```bash
# Add to ~/.bashrc or ~/.zshrc
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk
source ~/.bashrc  # or ~/.zshrc
```

---

### Required Files
You will be provided with three COBOL source files:
- `COBCALC.cbl` - Main controller program
- `COBLOAN.cbl` - Loan payment calculator subprogram
- `COBVALU.cbl` - Present value calculator subprogram

**Source**: These are IBM sample programs from the Debug for z/OS documentation.
**Download from**: https://www.ibm.com/docs/en/debug-for-zos/16.0.x?topic=mode-example-sample-cobol-program-debugging

### Required Tools
- Java 11 or higher
- Maven 3.6+
- IDE (VS Code, IntelliJ, or Eclipse)
- IBM Bob AI Assistant

---

## Step 1 - Understand the COBOL Code (5 minutes)

### Why this step?
Before converting legacy code, engineers must **fully understand** the business logic, data structures, and non-obvious patterns:
- COBOL-specific idioms (REDEFINES, UNSTRING, INSPECT)
- Financial calculation methods (ANNUITY, PRESENT-VALUE)
- Subprogram calling conventions (LINKAGE SECTION)
- Data type mappings (COMP, DISPLAY, PIC clauses)

This step shows that Agentic AI can perform a **deep technical analysis** of legacy code.

### Prompt
```
Analyze the COBOL financial calculator codebase and provide a comprehensive explanation 
of its functionality. Describe:

1. The overall program structure and flow
2. How COBCALC orchestrates the subprograms
3. The financial calculations performed (loan payments and present value)
4. Non-obvious COBOL patterns used (REDEFINES arrays, UNSTRING delimiters, 
   underscore placeholder technique)
5. Data type usage (COMP vs DISPLAY, PIC clauses)
6. The LINKAGE SECTION feedback mechanism

Create a Mermaid architecture diagram showing:
- Program relationships and CALL flow
- Data structures and their transformations
- Key methods and their purposes
- The calculation pipeline from input to output
```

### Expected Insights
Bob should identify:
- Hardcoded test data pattern (not production-ready)
- REDEFINES technique for array simulation
- Monthly rate conversion requirement (INTEREST / 12)
- Two-character feedback mechanism ("OK"/"NO")
- Underscore placeholder formatting technique
- Case-insensitive input handling via FUNCTION UPPER-CASE

---

## Step 2 - Convert to Java (10 minutes)

### Why this step?
Modern Java provides better maintainability, testability, and integration capabilities than legacy COBOL.

### Prompt
```
Convert the COBOL financial calculator to Java with the following requirements:

1. Use BigDecimal for all financial calculations (avoid floating-point errors)
2. Create separate classes for each calculator (LoanCalculator, PresentValueCalculator)
3. Implement a CalculationResult class to replace LINKAGE SECTION feedback
4. Preserve the original calculation logic exactly
5. Handle edge cases (zero interest, negative values, empty arrays)
6. Create a Main class that mimics COBCALC's orchestration
7. Use Maven for build management with JUnit 5 dependencies

Provide:
- Complete Java source code for all classes
- Maven pom.xml configuration
- Package structure (com.financial.calculator)
- Proper error handling and validation
```

### Key Conversion Patterns
- `PIC S9(9)V99 COMP` → `BigDecimal` with proper scale
- `PIC XX` → `String` or custom enum for status
- `FUNCTION ANNUITY` → Custom annuity formula implementation
- `FUNCTION PRESENT-VALUE` → NPV calculation with loop
- `UNSTRING ... DELIMITED BY` → `String.split()` with regex
- `INSPECT REPLACING` → `String.replace()`

### Deliverables
- `CalculationResult.java` - Result wrapper with success/failure status
- `LoanCalculator.java` - Loan payment calculator
- `PresentValueCalculator.java` - Present value calculator
- `Main.java` - Main controller
- `pom.xml` - Maven configuration

---

## Step 3 - Create Comprehensive Tests (8 minutes)

### Why this step?
Tests prevent regressions, validate conversion accuracy, and enable safe refactoring.

### Prompt
```
Create a comprehensive JUnit 5 test suite for the financial calculators:

1. Test with original COBOL test data to verify conversion accuracy
2. Test edge cases:
   - Zero interest rates
   - Single period loans
   - Negative cash flows
   - Empty input arrays
   - Very large numbers
3. Test error conditions:
   - Negative loan amounts
   - Invalid discount rates (≤ -1)
   - Zero or negative periods
4. Verify message formatting matches COBOL output
5. Test currency formatting ($X,XXX.XX)

Provide:
- LoanCalculatorTest.java with 8+ test cases
- PresentValueCalculatorTest.java with 10+ test cases
- Clear test names describing what is being tested
- Assertions that validate both values and messages
```

### Test Categories
- **Accuracy Tests**: Verify calculations match COBOL results
- **Edge Case Tests**: Zero interest, single cash flow, etc.
- **Validation Tests**: Reject invalid inputs appropriately
- **Format Tests**: Verify output message formatting
- **Boundary Tests**: Test with extreme values

### Expected Results
All tests should pass, demonstrating:
- Conversion accuracy (matches COBOL output)
- Proper error handling
- Edge case coverage

---

## Step 4 - Build Interactive UI (10 minutes)

### Why this step?
Legacy COBOL programs use hardcoded test data. Modern applications need interactive user interfaces.

### Prompt
```
Create a JavaFX or Swing GUI for the financial calculator with:

1. Tabbed interface with two tabs:
   - "Loan Calculator" tab
   - "Present Value Calculator" tab

2. Loan Calculator tab should have:
   - Input fields: Loan Amount, Annual Interest Rate (%), Number of Months
   - "Calculate" button
   - Results display area showing monthly payment
   - Input validation with error messages

3. Present Value Calculator tab should have:
   - Input fields: Discount Rate (%), Number of Periods
   - Dynamic cash flow input fields (add/remove capability)
   - "Calculate" button
   - Results display area showing present value
   - Input validation

4. Features:
   - Clear/Reset buttons
   - Currency formatting in results
   - Keyboard shortcuts (Enter to calculate)
   - Professional styling with proper layout
   - Error dialogs for invalid inputs

Provide complete source code and instructions to run the GUI.
```

### UI Requirements
- **Input Validation**: Real-time validation with visual feedback
- **Error Handling**: User-friendly error messages
- **Responsive Design**: Proper layout management
- **Accessibility**: Keyboard navigation support

### Deliverables
- `FinancialCalculatorGUI.java` - Main GUI class
- Updated `pom.xml` with JavaFX/Swing dependencies
- Instructions to run: `mvn javafx:run` or `mvn exec:java`

---

## Step 5 - Add REST API (7 minutes)

### Why this step?
Modern architectures use microservices. Wrap the calculators in a REST API for integration.

### Prompt
```
Create a Spring Boot REST API for the financial calculators:

1. Endpoints:
   - POST /api/loan/calculate
     Request: { "loanAmount": 30000, "annualRate": 0.09, "periods": 24 }
     Response: { "monthlyPayment": 1370.54, "message": "..." }
   
   - POST /api/presentvalue/calculate
     Request: { "discountRate": 0.12, "cashFlows": [50, 69, 83, 75, 44] }
     Response: { "presentValue": 231.36, "message": "..." }

2. Features:
   - Input validation with proper HTTP status codes
   - JSON request/response bodies
   - Error handling with meaningful messages
   - CORS configuration for web clients
   - Swagger/OpenAPI documentation

3. Provide:
   - REST controller classes
   - Request/Response DTOs
   - Updated pom.xml with Spring Boot dependencies
   - application.properties configuration
   - Instructions to run and test the API
```

### API Design
- **RESTful**: Proper HTTP methods and status codes
- **Validation**: Bean Validation annotations
- **Documentation**: Swagger UI at `/swagger-ui.html`
- **Testing**: Example curl commands

### Deliverables
- `LoanCalculatorController.java`
- `PresentValueCalculatorController.java`
- `LoanRequest.java` / `LoanResponse.java` DTOs
- `PresentValueRequest.java` / `PresentValueResponse.java` DTOs
- Updated `pom.xml` with Spring Boot starter web
- `application.properties` with server configuration

---

## Step 6 - Performance Comparison (Optional - 5 minutes)

### Why this step?
Validate that the Java implementation performs adequately compared to COBOL.

### Prompt
```
Create a performance benchmark comparing the Java implementation:

1. Create a benchmark harness that:
   - Runs 100,000 loan calculations
   - Runs 100,000 present value calculations
   - Measures execution time and memory usage
   - Compares BigDecimal vs double precision

2. Provide:
   - Benchmark code using JMH (Java Microbenchmark Harness)
   - Instructions to run benchmarks
   - Analysis of results
   - Recommendations for optimization if needed

3. Test scenarios:
   - Single-threaded performance
   - Multi-threaded performance (parallel streams)
   - Memory allocation patterns
```

### Expected Insights
- BigDecimal overhead vs double
- JVM warmup effects
- Optimization opportunities

---

## Step 7 - Documentation Generation (Optional - 5 minutes)

### Why this step?
Comprehensive documentation supports long-term maintenance and onboarding.

### Prompt
```
Generate comprehensive documentation for the Java financial calculator:

1. JavaDoc comments for all public methods
2. Architecture diagram showing:
   - Class relationships
   - Data flow
   - API endpoints (if REST API was created)
3. User guide with:
   - How to build and run
   - API usage examples
   - Configuration options
4. Migration guide documenting:
   - COBOL to Java mapping decisions
   - Known differences
   - Testing strategy

Generate using Maven site plugin and provide instructions to view.
```

### Documentation Deliverables
- JavaDoc HTML
- Architecture diagrams (Mermaid/PlantUML)
- User guide (Markdown)
- API documentation (Swagger)

---

## Summary & Key Takeaways

### What You've Accomplished
1. ✅ Analyzed legacy COBOL financial software
2. ✅ Converted to modern Java with proper design patterns
3. ✅ Created comprehensive test suite (19+ tests)
4. ✅ Built interactive user interface
5. ✅ Wrapped in REST API for microservices
6. ✅ Benchmarked performance
7. ✅ Generated complete documentation

### Key Modernization Patterns Learned
- **Data Type Mapping**: COBOL COMP → Java BigDecimal
- **Subprogram Conversion**: CALL/LINKAGE → Method calls/Return objects
- **Financial Precision**: Avoiding floating-point errors
- **Test-Driven Migration**: Validate conversion accuracy
- **UI Modernization**: From batch to interactive
- **API-First Design**: Enable integration with modern systems

### Real-World Applications
This workshop demonstrates patterns applicable to:
- Banking and financial services modernization
- Insurance policy calculation systems
- Payroll and benefits processing
- Inventory and pricing systems
- Any COBOL system with complex business logic

### Next Steps
- Apply these patterns to your own COBOL codebases
- Extend with additional features (reporting, audit trails)
- Integrate with modern data stores (PostgreSQL, MongoDB)
- Deploy to cloud platforms (AWS, Azure, IBM Cloud)
- Implement CI/CD pipelines for continuous modernization

---

## Appendix: Quick Reference

### Maven Commands
```bash
mvn clean compile          # Compile the project
mvn test                   # Run all tests
mvn exec:java             # Run the main application
mvn javafx:run            # Run JavaFX GUI (if created)
mvn spring-boot:run       # Run Spring Boot API (if created)
mvn package               # Build JAR file
```

### Expected Test Results
- **Total Tests**: 19
- **Loan Calculator Tests**: 8 (all passing)
- **Present Value Tests**: 11 (all passing)
- **Execution Time**: < 1 second

### Key Files Created
```
COBOL2JAVA/
├── pom.xml
├── README.md
├── src/
│   ├── main/java/com/financial/calculator/
│   │   ├── Main.java
│   │   ├── CalculationResult.java
│   │   ├── LoanCalculator.java
│   │   ├── PresentValueCalculator.java
│   │   ├── FinancialCalculatorGUI.java (Step 4)
│   │   └── controllers/ (Step 5)
│   └── test/java/com/financial/calculator/
│       ├── LoanCalculatorTest.java
│       └── PresentValueCalculatorTest.java
├── COBCALC.cbl (original)
├── COBLOAN.cbl (original)
└── COBVALU.cbl (original)
```

---

## Support & Resources

- **IBM Bob Documentation**: [Link to Bob docs]
- **COBOL to Java Migration Guide**: [Link to guide]
- **Sample Code Repository**: [Link to samples]
- **Community Forum**: [Link to forum]

---

**Workshop Version**: 1.0  
**Last Updated**: 2026-02-24  
**Estimated Duration**: 30-45 minutes  
**Difficulty Level**: Intermediate