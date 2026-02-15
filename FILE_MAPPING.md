# ShadowTrace - File Renaming Summary

## File Name Changes

Your files have been renamed for better clarity and professional presentation:

### Main Changes

1. **Converting_Cdata_To_Python.py** → **file_monitor.py**
   - Reason: More descriptive name that clearly indicates its purpose
   - This is the core monitoring engine

2. **Datacollector.c** → **file_scanner.c**
   - Reason: Better describes what the C library does
   - Matches the pattern of having descriptive module names

3. **Datacollector.h** → **file_scanner.h**
   - Reason: Header file should match the .c file name
   - Maintains consistency

4. **emailsenderforoneperson.py** → **email_reporter.py**
   - Reason: Shorter, more professional name
   - Removed "foroneperson" as it can be configured for any recipient

5. **FileChecker.py** → **shadowtrace.py**
   - Reason: Uses the project name as the main entry point
   - This is the standard convention (project name = main file)

### All Import Statements Updated

All files that import these modules have been automatically updated:
- shadowtrace.py now imports `file_monitor` and `email_reporter`
- All function calls updated to use new module names

### Security Improvements

**email_reporter.py** has been updated to:
- Remove hardcoded email credentials
- Use environment variables for security
- Provide helpful error messages
- Guide users through setup

### New Files Added

1. **README.md** - Comprehensive project documentation
2. **DOCUMENTATION.docx** - Detailed technical documentation
3. **requirements.txt** - Python dependencies list
4. **LICENSE** - MIT License
5. **SETUP_GUIDE.md** - GitHub setup instructions
6. **.gitignore** - Git ignore patterns

## How to Use the Renamed Files

### Quick Start

1. Make sure all files are in the same directory
2. Compile the C library:
   ```bash
   gcc -shared -o libcheckpass.so file_scanner.c -lkernel32
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Set up email:
   ```bash
   # Windows
   set SHADOWTRACE_EMAIL=your@gmail.com
   set SHADOWTRACE_PASSWORD=your-app-password
   set SHADOWTRACE_RECEIVER=alerts@example.com
   ```

5. Run the program:
   ```bash
   python shadowtrace.py
   ```

## File Structure

```
shadowtrace/
├── shadowtrace.py          # Main entry point (was FileChecker.py)
├── file_monitor.py         # Monitoring engine (was Converting_Cdata_To_Python.py)
├── file_scanner.c          # C library (was Datacollector.c)
├── file_scanner.h          # C header (was Datacollector.h)
├── email_reporter.py       # Email system (was emailsenderforoneperson.py)
├── requirements.txt        # NEW: Python dependencies
├── README.md               # NEW: Project documentation
├── DOCUMENTATION.docx      # NEW: Detailed guide
├── LICENSE                 # NEW: MIT License
├── SETUP_GUIDE.md          # NEW: GitHub setup guide
└── .gitignore              # NEW: Git ignore file
```

## Benefits of New Names

1. **Professional**: Names follow industry standards
2. **Clear**: Purpose is immediately obvious
3. **Consistent**: All files follow same naming convention
4. **Searchable**: Easier to find and remember
5. **GitHub-Ready**: Standard structure for open source projects

## No Breaking Changes

The functionality remains exactly the same. Only the file names and imports have changed.

---

✅ All files are ready for GitHub publication!
