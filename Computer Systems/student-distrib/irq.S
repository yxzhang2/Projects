
# irq.S - assembly interrupt functions
# vim:ts=4 noexpandtab

#define ASM     1

# extern key_handler_main
# extern rtc_handler_main
# extern sys_call_handler_main
# extern DIVIDE_ERROR_EXCP_MAIN
# extern DEBUG_EXCP_MAIN
# extern NMI_EXCP_MAIN
# extern BREAKPOINT_EXCP_MAIN
# extern OVERFLOW_EXCP_MAIN
# extern BOUND_RANGE_EXC_EXCP_MAIN
# extern INV_OPC_EXCP_MAIN
# extern DEVICE_NA_EXCP_MAIN
# extern DOUB_FAULT_EXCP_MAIN
# extern COP_SEG_OVR_EXCP_MAIN
# extern INV_TSS_EXCP_MAIN
# extern SEG_NT_PRE_EXCP_MAIN
# extern STK_FAULT_EXCP_MAIN
# extern GEN_PRO_EXCP_MAIN
# extern PGE_FAULT_EXCP_MAIN
# extern FPU_FLOAT_POINT_EXCP_MAIN
# extern ALIGN_CHK_EXCP_MAIN
# extern MACH_CHK_EXCP_MAIN
# extern SIMD_FLOAT_POINT_EXCP_MAIN


.globl key_handler
.globl rtc_handler
.globl sys_call_handler
.globl DIVIDE_ERROR_EXCP
.globl DEBUG_EXCP
.globl NMI_EXCP
.globl BREAKPOINT_EXCP
.globl OVERFLOW_EXCP
.globl BOUND_RANGE_EXC_EXCP
.globl INV_OPC_EXCP
.globl DEVICE_NA_EXCP
.globl DOUB_FAULT_EXCP
.globl COP_SEG_OVR_EXCP 
.globl INV_TSS_EXCP
.globl SEG_NT_PRE_EXCP
.globl STK_FAULT_EXCP
.globl GEN_PRO_EXCP
.globl PGE_FAULT_EXCP
.globl FPU_FLOAT_POINT_EXCP
.globl ALIGN_CHK_EXCP
.globl MACH_CHK_EXCP
.globl SIMD_FLOAT_POINT_EXCP



# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
DIVIDE_ERROR_EXCP:
	pusha
	CLD
	call DIVIDE_ERROR_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x1, calls the c counterpart 
# 
DEBUG_EXCP:
	pusha
	CLD
	call DEBUG_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
NMI_EXCP:
	pusha
	CLD
	call NMI_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
BREAKPOINT_EXCP:
	pusha
	CLD
	call BREAKPOINT_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
OVERFLOW_EXCP:
	pusha
	CLD
	call OVERFLOW_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
BOUND_RANGE_EXC_EXCP:
	pusha
	CLD
	call BOUND_RANGE_EXC_EXCP
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
INV_OPC_EXCP:
	pusha
	CLD
	call INV_OPC_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
DEVICE_NA_EXCP:
	pusha
	CLD
	call DEVICE_NA_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
DOUB_FAULT_EXCP:
	pusha
	CLD
	call DOUB_FAULT_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
COP_SEG_OVR_EXCP:
	pusha
	CLD
	call COP_SEG_OVR_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
INV_TSS_EXCP:
	pusha
	CLD
	call INV_TSS_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
SEG_NT_PRE_EXCP:
	pusha
	CLD
	call SEG_NT_PRE_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
STK_FAULT_EXCP:
	pusha
	CLD
	call STK_FAULT_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
GEN_PRO_EXCP:
	pusha
	CLD
	call GEN_PRO_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
PGE_FAULT_EXCP:
	pusha
	CLD
	call PGE_FAULT_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
FPU_FLOAT_POINT_EXCP:
	pusha
	CLD
	call FPU_FLOAT_POINT_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
ALIGN_CHK_EXCP:
	pusha
	CLD
	call ALIGN_CHK_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
MACH_CHK_EXCP:
	pusha
	CLD
	call MACH_CHK_EXCP_MAIN
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
SIMD_FLOAT_POINT_EXCP:
	pusha
	CLD
	call SIMD_FLOAT_POINT_EXCP_MAIN
	popa
	iret


# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
key_handler:
	pusha
	CLD
	call key_handler_main
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
rtc_handler:
	pusha
	CLD
	call rtc_handler_main
	popa
	iret
	
# DIVIDE_ERROR_EXCP
# exception handler for int 0x0, calls the c counterpart 
# 
sys_call_handler:
	pusha
	pushl %eax
	call sys_call_handler_main
	popl %eax
	popa
	iret