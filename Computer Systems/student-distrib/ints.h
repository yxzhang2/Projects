

#ifndef INTS_H
#define INTS_H

	extern void DIVIDE_ERROR_EXCP(void);
	extern void DEBUG_EXCP(void);          
	extern void NMI_EXCP(void);         
	extern void BREAKPOINT_EXCP(void);      
	extern void OVERFLOW_EXCP(void);      
	extern void BOUND_RANGE_EXC_EXCP (void);
	extern void INV_OPC_EXCP(void);       
	extern void DEVICE_NA_EXCP(void);     
	extern void DOUB_FAULT_EXCP(void);     
	extern void COP_SEG_OVR_EXCP(void);  
	extern void INV_TSS_EXCP(void);
	extern void SEG_NT_PRE_EXCP(void);
	extern void STK_FAULT_EXCP(void);
	extern void GEN_PRO_EXCP(void);
	extern void PGE_FAULT_EXCP(void);
	extern void FPU_FLOAT_POINT_EXCP(void);
	extern void ALIGN_CHK_EXCP(void);
	extern void MACH_CHK_EXCP(void);
	extern void SIMD_FLOAT_POINT_EXCP(void);
	extern void key_handler_main(void);
	extern void rtc_handler_main(void);
	extern void sys_call_handler_main(int call_id);

	
#endif