

#include "lib.h"
#include "kernel.c"
#include "ints.h"

#define KEYBOARD_DATA_PORT 0x60
#define KEYBOARD_STATUS_PORT 0x64

extern void DIVIDE_ERROR_EXCP_MAIN(void)
{
	printf("Error Found: Divide by Zero");
	cli();
	while(1)
}

extern void DEBUG_EXCP_MAIN(void)
{
	printf("Debug Exception Generated");
	cli();
	while(1)
}

extern void NMI_EXCP_MAIN(void)
{
	printf("NMI exception generated");
	cli();
	while(1)
}

extern void BREAKPOINT_EXCP_MAIN(void)
{
	printf("Breakpoint Found:");
	cli();
	while(1)
}

extern void OVERFLOW_EXCP_MAIN(void)
{
	printf("Overflow Exception Generated");
	cli();
	while(1)
}

extern void BOUND_RANGE_EXC_EXCP_MAIN(void)
{
	printf("Bound Range has been exceeded");
	cli();
	while(1)
}

extern void INV_OPC_EXCP_MAIN(void)
{
	printf("Invalid Opcode has been sent");
	while(1)
}

extern void DEVICE_NA_EXCP_MAIN(void)
{
	printf("Device is not available at");
	cli();
	while(1)
}

extern void DOUB_FAULT_EXCP_MAIN(void)
{
	printf("Double Fault has been generated, aborting..." );
	cli();
	while(1)
}

extern void COP_SEG_OVR_EXCP_MAIN(void)
{
	printf("Coprocessor Segment has been Overrun" );
	cli();
	while(1)
}

extern void INV_TSS_EXCP_MAIN(void)
{
	printf("TSS error detected" );
	cli();
	while(1)
}

extern void SEG_NT_PRE_EXCP_MAIN(void)
{
	printf("flag is not present" );
	cli();
	while(1)
}

extern void STK_FAULT_EXCP_MAIN(void)
{
	printf("Stack Segfault Condition has been detected" );
	cli();
	while(1)
}

extern void GEN_PRO_EXCP_MAIN(void)
{
	printf("General Protection Violation detected" );
	cli();
	while(1)
}

extern void PGE_FAULT_EXCP_MAIN(void)
{
	printf("Error with paging" );
	cli();
	while(1)
}

extern void FPU_FLOAT_POINT_EXCP_MAIN(void)
{
	printf("Floating point error detected: FPU" );
	cli();
	while(1)
}

extern void ALIGN_CHK_EXCP_MAIN(void)
{
	printf("Unaligned memory operand detected" );
	cli();
	while(1)
}

extern void MACH_CHK_EXCP_MAIN(void)
{
	printf("Internal Machine or Bus error detected" );
	cli();
	while(1)
}

extern void SIMD_FLOAT_POINT_EXCP_MAIN(void)
{
	printf("Processor has detected SIMD float-point exception " );
	cli();
	while(1)
}


extern void key_handler_main(void)
{
	uint8_t status;
	uint8_t keycode;

	// write EOI
	sendEOI(1);

	status = inb(KEYBOARD_STATUS_PORT);
	// Lowest bit of status will be set if buffer is not empty
	if (status & 0x01) {
		keycode = inb(KEYBOARD_DATA_PORT);
		if(keycode < 0)
			return;
		printf(keycode);
	}
}

extern void rtc_handler_main(void)
{
	// write EOI
	sendEOI(8);
	test_interrupts();

}

extern void sys_call_handler_main(int call_id)
{
	
	printf("system call made: %d", call_id);

}

/*Exception function array*/

extern void* func_arr[32] = 
{
	DIVIDE_ERROR_EXCP,    //0
	DEBUG_EXCP,           //1
	NMI_EXCP,             //2 (NMI)
	BREAKPOINT_EXCP,      //3
	OVERFLOW_EXCP,        //4
	BOUND_RANGE_EXC_EXCP, //5
	INV_OPC_EXCP,         //6
	DEVICE_NA_EXCP,       //7
	DOUB_FAULT_EXCP,      //8
	COP_SEG_OVR_EXCP      //9 (Coprocessor Segment Overrun)
	INV_TSS_EXCP,         //10
	SEG_NT_PRE_EXCP,      //11
	STK_FAULT_EXCP,       //12
	GEN_PRO_EXCP,         //13
	PGE_FAULT_EXCP,       //14
	0x0,                    //15
	FPU_FLOAT_POINT_EXCP, //16
	ALIGN_CHK_EXCP,       //17
	MACH_CHK_EXCP,        //18
	SIMD_FLOAT_POINT_EXCP,//19
	0x0,                  //20-31unused
	0x0,
	0x0,
	0x0,
	0x0,
	0x0,
	0x0,
	0x0,
	0x0,
	0x0,
	0x0,
	0x0
};




