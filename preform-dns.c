/* Compatibility with the no-op multicast-query functions in newer Wine.
 * These functions do not discover printers or invoke query callbacks.
 * See https://github.com/wine-mirror/wine/blob/master/dlls/dnsapi/main.c
 */
#include <windows.h>

LONG WINAPI DnsStartMulticastQuery(void *request, void *handle)
{
    (void)request;
    (void)handle;
    return ERROR_SUCCESS;
}

LONG WINAPI DnsStopMulticastQuery(void *handle)
{
    (void)handle;
    return ERROR_SUCCESS;
}
