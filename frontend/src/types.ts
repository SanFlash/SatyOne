export type Category={id:number;slug:string;name:string;description:string;icon:string}
export type Command={id:number;slug:string;name:string;syntax:string;description:string;instruction_template:string;example_input:string;example_output:string;difficulty:string;status:string;tags:string[];limitations:string;category:Category}
export type Provider={id:number;slug:string;name:string;description:string;docs_url:string;integration_status:string}
export type Workflow={id:number;slug:string;name:string;description:string;category:string;difficulty:string;steps:string[]}

export type SavedPrompt={id:number;title:string;prompt:string;owner_key:string}
