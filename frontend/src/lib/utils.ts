import format from "date-fns/format"
import parseISO from "date-fns/parseISO"

export function formatTime(dateTime: string): string {
    return format(parseISO(dateTime), "PPpp")
}


export abstract class BaseSubmitHandler {
    public submitBtn: HTMLButtonElement
    public reEnableTimeoutMs = 2000

    async submit(e: Event) {
        e.preventDefault()
        if (this.submitBtn.disabled) {
            return
        }
        this.submitBtn.disabled = true

        this.onStart()
        try {
            const r = this.doSubmit()
            if (r instanceof Promise) {
                await r
            }
        } catch (err) {
            this.replaceClasses("btn-danger")
            setTimeout(() => this.reEnableSubmit(), this.reEnableTimeoutMs)
            if (!this.onError(err)) {
                throw err
            }
        }

        this.replaceClasses("btn-success")
        this.onSuccess()
        setTimeout(() => this.reEnableSubmit(), this.reEnableTimeoutMs)
    }

    private replaceClasses(to: string) {
        this.submitBtn.classList.remove("btn-success", "btn-primary", "btn-danger")
        this.submitBtn.classList.add(to)
    }

    private reEnableSubmit() {
        this.submitBtn.disabled = false
        this.replaceClasses("btn-primary")
    }

    protected abstract doSubmit()

    protected onStart() {}

    protected onSuccess() {}

    protected onError(err: Error): boolean {
        return false
    }
}
