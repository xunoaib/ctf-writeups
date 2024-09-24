# Revioli, Revioli, give me the formeoli

## Description

Can you unlock the secret formula?

Author: Shiloh Smiles (arcticx)

## Files

* [revioli](revioli)

## Solution

We're given a binary program `revioli` which prompts us for a password before printing a success/error message.

We can import the executable into Ghidra, then decompile functions like `main` to roughly see what they're doing:
```
undefined8 main(void)

{
  int iVar1;
  size_t sVar2;
  long in_FS_OFFSET;
  char local_318 [256];
  char local_218 [256];
  undefined local_118 [264];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  gen_correct_flag(local_218);
  assemble_flag(local_218,local_118);
  printf("Enter-a the password-a: ");
  fgets(local_318,0x100,stdin);
  sVar2 = strcspn(local_318,"\n");
  local_318[sVar2] = '\0';
  iVar1 = strcmp(local_318,local_218);
  if (iVar1 == 0) {
    printf("Congratulations! The flag is: %s\n",local_118);
  }
  else {
    puts("No toucha my spaget!");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

- Functions `gen_correct_flag` and `assemble_flag` are called **immediately** in `main` and seem to generate the flag... before any user interaction occurs. This means the flag is likely loaded into memory somewhere.
- To verify this, we can use a debugger like `gdb` to inspect the program while it's running.

Run `gdb revioli`
Set a breakpoint on `assemble_flag` (using `b assemble_flag`).
Type `run` to begin running the program. It should eventually hit the breakpoint and pause execution inside `assemble_flag`.
Type `finish` to continue executing until the current function returns (back to `main`).
Now inspect stack memory (specifically, the local variables):

All Steps:
```
gdb revioli
info functions
b assemble_flag
run
finish
```

`PCTF{ITALY_01123581321345589144233377}`
