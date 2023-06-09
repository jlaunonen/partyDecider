/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import * as runtime from '../runtime';
import type {
  App,
  Ballot,
  HTTPValidationError,
  Message,
  VotingSession,
  VotingSessionResult,
} from '../models';
import {
    AppFromJSON,
    AppToJSON,
    BallotFromJSON,
    BallotToJSON,
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
    MessageFromJSON,
    MessageToJSON,
    VotingSessionFromJSON,
    VotingSessionToJSON,
    VotingSessionResultFromJSON,
    VotingSessionResultToJSON,
} from '../models';

export interface GetVotingResultRequest {
    voteSessionKey: string;
}

export interface SubmitBallotRequest {
    voteSessionKey: string;
    ballot: Ballot;
}

/**
 * 
 */
export class PublicApi extends runtime.BaseAPI {
    makeQueryParameters(queryParameters: any): string {
        if (Object.keys(queryParameters).length !== 0) {
            // only add the querystring to the URL if there are query parameters.
            // this is done to avoid urls ending with a "?" character which buggy webservers
            // do not handle correctly sometimes.
            return '?' + this.configuration.queryParamsStringify(queryParameters);
        }
        return "";
    }

    getApps_Path(): string {
        const queryParameters: any = {};


        const path = `/api/apps`;

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Get enabled apps/games.
     */
    async getAppsRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<App>>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/apps`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(AppFromJSON));
    }

    /**
     * Get enabled apps/games.
     */
    async getApps(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<App>> {
        const response = await this.getAppsRaw(initOverrides);
        return await response.value();
    }

    getVotingList_Path(): string {
        const queryParameters: any = {};


        const path = `/api/voting`;

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Get currently active voting sessions.
     */
    async getVotingListRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<VotingSession>>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/voting`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(VotingSessionFromJSON));
    }

    /**
     * Get currently active voting sessions.
     */
    async getVotingList(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<VotingSession>> {
        const response = await this.getVotingListRaw(initOverrides);
        return await response.value();
    }

    getVotingResult_Path(requestParameters: GetVotingResultRequest): string {
        if (requestParameters.voteSessionKey === null || requestParameters.voteSessionKey === undefined) {
            throw new runtime.RequiredError('voteSessionKey','Required parameter requestParameters.voteSessionKey was null or undefined when calling getVotingResult.');
        }

        const queryParameters: any = {};


        const path = `/api/voting/{vote_session_key}`.replace(`{${"vote_session_key"}}`, encodeURIComponent(String(requestParameters.voteSessionKey)));

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Get voting session result.
     */
    async getVotingResultRaw(requestParameters: GetVotingResultRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<VotingSessionResult>> {
        if (requestParameters.voteSessionKey === null || requestParameters.voteSessionKey === undefined) {
            throw new runtime.RequiredError('voteSessionKey','Required parameter requestParameters.voteSessionKey was null or undefined when calling getVotingResult.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/voting/{vote_session_key}`.replace(`{${"vote_session_key"}}`, encodeURIComponent(String(requestParameters.voteSessionKey))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => VotingSessionResultFromJSON(jsonValue));
    }

    /**
     * Get voting session result.
     */
    async getVotingResult(requestParameters: GetVotingResultRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<VotingSessionResult> {
        const response = await this.getVotingResultRaw(requestParameters, initOverrides);
        return await response.value();
    }

    submitBallot_Path(requestParameters: SubmitBallotRequest): string {
        if (requestParameters.voteSessionKey === null || requestParameters.voteSessionKey === undefined) {
            throw new runtime.RequiredError('voteSessionKey','Required parameter requestParameters.voteSessionKey was null or undefined when calling submitBallot.');
        }

        if (requestParameters.ballot === null || requestParameters.ballot === undefined) {
            throw new runtime.RequiredError('ballot','Required parameter requestParameters.ballot was null or undefined when calling submitBallot.');
        }

        const queryParameters: any = {};


        const path = `/api/voting/{vote_session_key}`.replace(`{${"vote_session_key"}}`, encodeURIComponent(String(requestParameters.voteSessionKey)));

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Submit ballot for voting session.
     */
    async submitBallotRaw(requestParameters: SubmitBallotRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Message>> {
        if (requestParameters.voteSessionKey === null || requestParameters.voteSessionKey === undefined) {
            throw new runtime.RequiredError('voteSessionKey','Required parameter requestParameters.voteSessionKey was null or undefined when calling submitBallot.');
        }

        if (requestParameters.ballot === null || requestParameters.ballot === undefined) {
            throw new runtime.RequiredError('ballot','Required parameter requestParameters.ballot was null or undefined when calling submitBallot.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/api/voting/{vote_session_key}`.replace(`{${"vote_session_key"}}`, encodeURIComponent(String(requestParameters.voteSessionKey))),
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: BallotToJSON(requestParameters.ballot),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => MessageFromJSON(jsonValue));
    }

    /**
     * Submit ballot for voting session.
     */
    async submitBallot(requestParameters: SubmitBallotRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Message> {
        const response = await this.submitBallotRaw(requestParameters, initOverrides);
        return await response.value();
    }

}
